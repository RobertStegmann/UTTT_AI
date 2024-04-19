import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import GameState as g
import numpy

import GameState as g
import TicTacToeAI as AI
import time 
import Heuristics as h
import copy

BATCH_SIZE = 200 # Must be a multiple of 8
DATA_SET_SIZE = 10000
MAX_BOARD = 82

import Model as m

class Trainer:
    def __init__(self,device,learning_rate = 0.0001,file_name='HeuristicNetwork.pth',load_file_name=None,save_file_name=None,newModel = False, stat_file = "TrainingStats.csv",adam=True):
        if load_file_name is None:
            self.load_file_name = file_name
        else:
            self.load_file_name = load_file_name
            
        if save_file_name is None:
            self.save_file_name = file_name
        else:
            self.save_file_name = save_file_name
            
        self.device = device
        
            
        self.loss = nn.CrossEntropyLoss()
        self.stat_file = stat_file        
        if (newModel or not m.HeuristicNetwork.fileExists(self.load_file_name)):
            self.model = m.HeuristicNetwork().to(self.device)
            self.optimizer = None
            if (adam):
                self.optimizer = torch.optim.Adam(self.model.parameters(),learning_rate)
            else:
                self.optimizer = torch.optim.SGD(self.model.parameters(),learning_rate)
            
            self.epoch = 1 
            self.time = 0
        else:
            loaded_data = m.HeuristicNetwork.load_train(self.load_file_name,device=self.device,adam=adam)
            self.model = loaded_data[0].to(self.device)
            self.optimizer = loaded_data[1]
            self.epoch = loaded_data[2] 
            self.time = loaded_data[3]   
    

    def generate_and_train(self,AI_1:AI.TicTacToeAI, AI_2:AI.TicTacToeAI, train_games = 0,train_time = 0,max_boards = MAX_BOARD,batch_size = BATCH_SIZE):
        
        game = g.GameState()
        Player1 = AI_1
        Player2 = AI_2

        start = time.time()
        gameNum = 0
        
        gamestate_list = []
        
        batch_board_list = torch.empty((0,3,9,9),dtype=float)
        batch_boards_won_list = torch.empty((0,3,3,3),dtype=float)
        batch_playable_board_list = torch.empty((0,1,3,3),dtype=float)
        
        label_list = torch.empty((0,3),dtype=float)
        
        batch_time = []
        
        length = 0
        accuracy_list = []
        loss_list = []
        
        if (self.time == 0) :
            start_time = -1
        else:
            start_time = time.time()
        
        buffer = batch_size % 8
          
        if (buffer == 0):
            batch_size = batch_size 
        else:        
            batch_size = batch_size + (8 - buffer)
        
        
        if (train_time == 0 and train_games == 0):
            print("No training length specified! Defaulting to 30 minutes")
            train_time = 1800
        player_flag = True
        
        while ((train_games == 0 or gameNum < train_games) and (train_time == 0 or (time.time() - start) < train_time)):  
            if (player_flag):
                Player1 = AI_1
                Player2 = AI_2
                player_flag = False
            else:
                Player1 = AI_2
                Player2 = AI_1
                player_flag = True
                
            gamestate_list  = []
            
            game = g.GameState()
            Player1.initialize()
            Player2.initialize()
            
            while (game.gameWon == g.NO_WIN):
                if (game.currentTurn == g.X_VAL):
                    moveAI = Player1.chooseMove(game)
                    gamestate_list .append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                else:
                    moveAI = Player2.chooseMove(game)
                    gamestate_list .append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                    
            length = len(gamestate_list )
            first = 0  
             
            if (max_boards < length):
                first = length-max_boards
            else:
                first = 0    
                
            for b in range(first,length):
                input = m.HeuristicNetwork.gameToTorch_dataset(gamestate_list[b]) 
                batch_board_list = torch.cat((batch_board_list,input[0]), dim = 0)
                batch_boards_won_list = torch.cat((batch_boards_won_list,input[1]), dim = 0)
                batch_playable_board_list = torch.cat((batch_playable_board_list,input[2]), dim = 0)
                
                label = None
                if (game.gameWon == g.GAME_WON):
                    if (gamestate_list[b].currentTurn == game.currentTurn):
                        label = torch.tensor([[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],dtype=float)   
                    else:
                        label = torch.tensor([[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],dtype=float)        
                else: 
                    label = torch.tensor([[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],dtype=float)
                    
                label_list = torch.cat((label_list,label), dim = 0) 
                            
                if (batch_board_list.size(dim=0) == batch_size):
                    stats = self.run_generated_batch((batch_board_list.to(self.device).float(),batch_boards_won_list.to(self.device).float(),batch_playable_board_list.to(self.device).float()),label_list.to(self.device).float(),batch_size)
                    accuracy_list.append(stats[0])
                    loss_list.append(stats[1])
                    
                    batch_board_list = torch.empty((0,3,9,9),dtype=float)
                    batch_boards_won_list = torch.empty((0,3,3,3),dtype=float)
                    batch_playable_board_list = torch.empty((0,1,3,3),dtype=float)
                    
                    label_list = torch.empty((0,3),dtype=float)
                    
                    if (start_time == -1):
                        start_time = time.time()
                        batch_time.append(self.time)
                    else:
                        batch_time.append(((time.time()-start_time)+self.time))              
            
            gameNum += 1
            Player1.cleanUp()
            Player2.cleanUp()
            
        if (len(batch_time) > 0):              
            self.record_training_stats(accuracy_list, loss_list, batch_time)    
            self.model.save(self.optimizer,self.epoch,batch_time[len(batch_time)-1],file_name=self.save_file_name)
        else:
            print("No training done! Insufficent parameters")
            
    def generate_dataset(self,AI_1:AI.TicTacToeAI, AI_2:AI.TicTacToeAI, max_games = 0,max_time = 0, max_boards = MAX_BOARD, file_name = 'dataset.npz'):    
        model_folder_path = './data/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)  
        
        file_name = os.path.join(model_folder_path, file_name)     
            
        game = g.GameState()
        Player1 = AI_1
        Player2 = AI_2

        start = time.time()
        gameNum = 0
        
        gamestate_list = []
        
        board_list = None
        boards_won_list = None
        playable_board_list = None
        
        label_list = None  
        
        if os.path.exists(file_name):
            loaded = numpy.load(file_name)
            
            board_list = torch.from_numpy(loaded['boards'])
            boards_won_list = torch.from_numpy(loaded['boards_won'])
            playable_board_list = torch.from_numpy(loaded['playable_boards'])
            label_list = torch.from_numpy(loaded['labels'])
        else:
            board_list = torch.empty((0,3,9,9),dtype=float)
            boards_won_list = torch.empty((0,3,3,3),dtype=float)
            playable_board_list = torch.empty((0,1,3,3),dtype=float)
           
            label_list = torch.empty((0,3),dtype=float)  
        
        initial_size = label_list.size(dim=0)
        
        if (max_time == 0 and max_games == 0):
            print("No training length specified! Defaulting to 30 minutes")
            max_time = 1800
            
        player_flag = True
        
        while ((max_games == 0 or gameNum < max_games) and (max_time == 0 or (time.time() - start) < max_time)):  
            if (player_flag):
                Player1 = AI_1
                Player2 = AI_2
                player_flag = False
            else:
                Player1 = AI_2
                Player2 = AI_1
                player_flag = True
                
            gamestate_list  = []
            game = g.GameState()
            Player1.initialize()
            Player2.initialize()
            
            while (game.gameWon == g.NO_WIN):
                if (game.currentTurn == g.X_VAL):
                    moveAI = Player1.chooseMove(game)
                    gamestate_list .append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                else:
                    moveAI = Player2.chooseMove(game)
                    gamestate_list .append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                    
            length = len(gamestate_list)
            first = 0  
             
            if (max_boards < length):
                first = length-max_boards
            else:
                first = 0    
                
            for b in range(first,length):
                input = m.HeuristicNetwork.gameToTorch_dataset(gamestate_list[b]) 
                board_list = torch.cat((board_list,input[0]), dim = 0)
                boards_won_list = torch.cat((boards_won_list,input[1]), dim = 0)
                playable_board_list = torch.cat((playable_board_list,input[2]), dim = 0)
                
                label = None
                if (game.gameWon == g.GAME_WON):
                    if (gamestate_list[b].currentTurn == game.currentTurn):
                        label = torch.tensor([[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],dtype=float)   
                    else:
                        label = torch.tensor([[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],dtype=float)        
                else: 
                    label = torch.tensor([[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],dtype=float)
                    
                label_list = torch.cat((label_list,label), dim = 0)            
            
            gameNum += 1
            Player1.cleanUp()
            Player2.cleanUp()
        # save to file        
        print("Created",label_list.size(dim=0)-initial_size,"items",flush=True)
        print("Total Dataset Size: ",label_list.size(dim=0),"items",flush=True)         
        
        #torch.save((board_list,boards_won_list,playable_board_list,label_list),f = file_name + ".pt")
        numpy.savez_compressed(file_name, boards = board_list.numpy(), boards_won = boards_won_list.numpy(), playable_boards = playable_board_list.numpy(), labels = label_list.numpy())
         
        
    def train_from_file (self, max_epochs = 0, max_time = 0, number_of_batches = 10,  training_file = 'dataset.npz', validation_file = None):   
        model_folder_path = './data/'
        if not os.path.exists(model_folder_path):
            print("ERROR: Dataset does not exist!")
            return
        
        file_name = os.path.join(model_folder_path, training_file) 
        
        if not os.path.exists(file_name):
            print("ERROR: Dataset does not exist!")
            return
        
        validation = False
        v_boards = None
        v_boards_won = None
        v_playable_boards = None
        v_labels = None
        if (not validation_file is None):
            v_file = os.path.join(model_folder_path, validation_file)
            if os.path.exists(v_file):
                v_loaded = numpy.load(v_file)
                v_boards = torch.from_numpy(v_loaded['boards']).to(self.device).float()
                v_boards_won = torch.from_numpy(v_loaded['boards_won']).to(self.device).float()
                v_playable_boards = torch.from_numpy(v_loaded['playable_boards']).to(self.device).float()
                v_labels = torch.from_numpy(v_loaded['labels']).to(self.device).float()
                validation = True
            
            
        train_loaded = numpy.load(file_name)
        
        epoch = 0
        start = time.time()
        
        train_boards = torch.from_numpy(train_loaded['boards']).to(self.device).float()
        train_boards_won = torch.from_numpy(train_loaded['boards_won']).to(self.device).float()
        train_playable_boards = torch.from_numpy(train_loaded['playable_boards']).to(self.device).float()
        train_labels = torch.from_numpy(train_loaded['labels']).to(self.device).float()
        
        total_size = train_labels.size(dim=0)
        
        v_size = 0
        if (validation):
            v_size = v_labels.size(dim=0)
        
        
        if (max_time == 0 and max_epochs == 0):
            print("No training length specified! Defaulting to 30 minutes")
            max_time = 1800
            
        s = 0
        e = 0
        increment = total_size // number_of_batches
        
        train_accuracy = []
        train_loss = []
        epoch_time = []
        
        v_accuracy = []
        v_loss = []
        
        if (self.time == 0) :
            start_time = -1
        else:
            start_time = time.time()
            
        #last_time = self.time
        
        while ((max_epochs == 0 or epoch < max_epochs) and (max_time == 0 or (time.time() - start) < max_time)):
            correct = 0
            loss_sum = 0
            #s_time = time.time()
            for i in range(0, number_of_batches):
                s = i * increment
                e = (i+1) * increment
                
                if (e > total_size):
                    e = total_size
                    
                inputs = (train_boards[s:e,],train_boards_won[s:e,],train_playable_boards[s:e,])
                labels = train_labels[s:e,]
                batch_size = labels.size(dim=0)
                
                self.optimizer.zero_grad()
                output = self.model(inputs)
                
                for i in range(0,batch_size):
                    if (output[i].argmax().item() == labels[i].argmax().item()):
                        correct += 1
                        
                loss = self.loss(output,labels)
                loss_sum += loss.item()
                loss.backward()
                self.optimizer.step()   
            
            #epoch_length = time.time() - s_time
            
            train_accuracy.append(correct/total_size)
            train_loss.append(loss_sum/number_of_batches)
            print("Epoch",epoch+self.epoch,"done!")
            
            if (start_time == -1):
                start_time = time.time()
                epoch_time.append(self.time)
            else:
                epoch_time.append(((time.time()-start_time)+self.time))       
                
            # if (last_time == 0):
            #     t_time = 0
            # else:
            #     t_time = epoch_length + last_time
                
            # epoch_time.append(t_time)   
            # last_time = t_time
            
            if (validation):
                correct = 0
                loss_sum = 0
                with torch.no_grad():
                    inputs = (v_boards,v_boards_won,v_playable_boards)
                    labels = v_labels
                    v_size = labels.size(dim=0)
                    
                    self.optimizer.zero_grad()
                    output = self.model(inputs)
                    
                    for i in range(0,v_size):
                        if (output[i].argmax().item() == labels[i].argmax().item()):
                            correct += 1
                            
                    loss = self.loss(output,labels)
                
                    v_accuracy.append(correct/v_size)
                    v_loss.append(loss.item()) 
            
            epoch += 1
                    
        # Record the stats
        if (len(epoch_time) > 0):              
            self.record_stats(train_accuracy, train_loss,v_accuracy,v_loss, epoch_time)    
            self.model.save(self.optimizer,self.epoch,epoch_time[len(epoch_time)-1],file_name=self.save_file_name)
        else:
            print("No training done! Insufficent parameters")
                
    
    def run_generated_batch(self,inputs,labels,batch_size):
        correct_sum = 0
        
        self.optimizer.zero_grad()
        output = self.model(inputs)
        
        for i in range(0,batch_size):
            if (output[i].argmax().item() == labels[i].argmax().item()):
                correct_sum += 1
                
        loss = self.loss(output,labels)
        loss_val = loss.item()
        loss.backward()
        self.optimizer.step()
        
        return (correct_sum/batch_size,loss_val)
    
    def dataset_shape(file_name):
        model_folder_path = './data/'
        if not os.path.exists(model_folder_path):
            print("ERROR: Dataset does not exist!")
            return
        
        file_name = os.path.join(model_folder_path, file_name) 
        
        if not os.path.exists(file_name):
            print("ERROR: Dataset does not exist!")
            return
        
        loaded = numpy.load(file_name)
        size = numpy.shape(loaded['labels'])
        print(size)
        return size
    
    def merge_dataset(file_name1, file_name2, output_file = "combined_dataset.pt"):
        model_folder_path = './data/'
        if not os.path.exists(model_folder_path):
            print("ERROR: Dataset does not exist!")
            return
        
        file_name1 = os.path.join(model_folder_path, file_name1) 
        
        if not os.path.exists(file_name1):
            print("ERROR: Dataset 1 does not exist!")
            return
        
        file_name2 = os.path.join(model_folder_path, file_name2) 
        
        if not os.path.exists(file_name2):
            print("ERROR: Dataset 2 does not exist!")
            return
        
        loaded1 = numpy.load(file_name1)
        boards1 = torch.from_numpy(loaded1['boards'])
        boards_won1 = torch.from_numpy(loaded1['boards_won'])
        playable_boards1 = torch.from_numpy(loaded1['playable_boards'])
        labels1 = torch.from_numpy(loaded1['labels'])
        
        loaded2 = numpy.load(file_name2)
        boards2 = torch.from_numpy(loaded2['boards'])
        boards_won2 = torch.from_numpy(loaded2['boards_won'])
        playable_boards2 = torch.from_numpy(loaded2['playable_boards'])
        labels2 = torch.from_numpy(loaded2['labels'])
        
        board_list = torch.cat((boards1,boards2), dim = 0)
        boards_won_list = torch.cat((boards_won1,boards_won2), dim = 0)  
        playable_board_list = torch.cat((playable_boards1,playable_boards2), dim = 0)  
        label_list = torch.cat((labels1,labels2), dim = 0)  
        
        output_file = os.path.join(model_folder_path, output_file) 
        
        numpy.savez_compressed(output_file, boards = board_list.numpy(), boards_won = boards_won_list.numpy(), playable_boards = playable_board_list.numpy(), labels = label_list.numpy())

    
    def record_training_stats(self, accuracy, loss, time):
        length = len(accuracy)
        
        model_folder_path = './NeuralNet/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, self.stat_file)
        file = open(file_name, "a")
        
        for i in range(0,length):
            file.write(str(accuracy[i]) + "," + str(loss[i]) + "," + str(time[i]) + "\n")
        file.close()
        self.epoch += length
        
    def record_stats(self, train_accuracy, train_loss, test_accuracy, test_loss, time):
        length = len(train_accuracy)
        
        model_folder_path = './NeuralNet/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, self.stat_file)
        file = open(file_name, "a")
        if (len(test_accuracy) == length):
            for i in range(0,length):
                file.write(str(train_accuracy[i]) + "," + str(train_loss[i]) + "," + str(test_accuracy[i]) + "," + str(test_loss[i]) + ","+ str(time[i]) + "\n")
        else:
            for i in range(0,length):
                file.write(str(train_accuracy[i]) + "," + str(train_loss[i]) + ",0,0,"+ str(time[i]) + "\n")
        file.close()
        self.epoch += length
        
        
    
        
        