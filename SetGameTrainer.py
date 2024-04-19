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

EPOCH_SIZE = 200 
MAX_BOARD = 82

import Model as m

class SetGameTrainer:
    def __init__(self,learning_rate = 0.0001,file_name='HeuristicNetwork.pth',load_file_name=None,save_file_name=None, stat_file = "SetGameStats.csv"):
        if load_file_name is None:
            self.load_file_name = file_name
        else:
            self.load_file_name = load_file_name
            
        if save_file_name is None:
            self.save_file_name = file_name
        else:
            self.save_file_name = save_file_name
            
        self.loss = nn.CrossEntropyLoss()
        self.stat_file = stat_file        
        self.model = m.HeuristicNetwork()
        self.optimizer = torch.optim.Adam(self.model.parameters(),learning_rate)
        self.epoch = 1 

    def train(self,AI_1:AI.TicTacToeAI, AI_2:AI.TicTacToeAI, sampleSize = 1, epochs = 1,train_time = 0,max_boards = MAX_BOARD):
        
        game = g.GameState()
        Player1 = AI_1
        Player2 = AI_2

        start = time.time()
        gameNum = 0
        
        board_list = []
        epoch_list = []
        label_list = []
        length = 0
        accuracy_list = []
        loss_list = []
        
        if (train_time == 0 and epochs == 0):
            print("No training length specified! Defaulting to 30 minutes")
            train_time = 1800
        player_flag = True
        
        board_count = 0
        
        while (board_count < sampleSize):     
            if (player_flag):
                Player1 = AI_1
                Player2 = AI_2
                player_flag = False
            else:
                Player1 = AI_2
                Player2 = AI_1
                player_flag = True
                
            board_list = []
            game = g.GameState()
            Player1.initialize()
            Player2.initialize()
            
            while (game.gameWon == g.NO_WIN):
                if (game.currentTurn == g.X_VAL):
                    moveAI = Player1.chooseMove(game)
                    board_list.append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                else:
                    moveAI = Player2.chooseMove(game)
                    board_list.append(copy.deepcopy(game))
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])
                    
            length = len(board_list)-1
            first = -1  
             
            if (max_boards < length):
                first = length-max_boards
            else:
                first = -1    
                
            for b in range(length,first,-1):    
                if (board_count < sampleSize):
                    epoch_list.append(m.HeuristicNetwork.gameToTorch(board_list[b]))
                    if (game.gameWon == g.GAME_WON):
                        if (board_list[b].currentTurn == game.currentTurn):
                            label_list.append(torch.tensor([1,0,0],dtype=float))
                        else:
                            label_list.append(torch.tensor([0,1,0],dtype=float))         
                    else:  
                        label_list.append(torch.tensor([0,0,1],dtype=float))    
                    board_count += 1        
      
            Player1.cleanUp()
            Player2.cleanUp()
            
            
        epochCount = 0
        
        while ((epochs == 0 or epochCount < epochs) and (train_time == 0 or (time.time() - start) < train_time)): 
            stats = self.runBatch(epoch_list,label_list)
            accuracy_list.append(stats[0])
            loss_list.append(stats[1])
            epochCount += 1
        
                      
        self.recordStats(accuracy_list, loss_list)    
        
    
    def runBatch(self,inputs,labels):
        correct_sum = 0
        loss_sum = 0
        j = 0
        for i in range(0,EPOCH_SIZE):
            self.optimizer.zero_grad()
            output = self.model(inputs[j])
            print(output,labels[j])
            #print(output.argmax().item(), labels[i].argmax().item())
            if (output.argmax().item() == labels[j].argmax().item()):
                correct_sum += 1
            loss = self.loss(output,labels[j])
            print(loss)
            loss_sum += loss.item()
            loss.backward()
            self.optimizer.step()
            j += 1
            if (j == len(inputs)):
                j = 0
        
        return (correct_sum/EPOCH_SIZE,loss_sum/EPOCH_SIZE)
    
    def recordStats (self, accuracy, loss):
        length = len(accuracy)
        
        model_folder_path = './NeuralNet/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, self.stat_file)
        file = open(file_name, "a")
        
        for i in range(0,length):
            file.write(str(accuracy[i]) + "," + str(loss[i]) + "\n")
        file.close()
        self.epoch += length
        
        