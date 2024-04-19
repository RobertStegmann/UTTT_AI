import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import GameState as g
import numpy

class HeuristicNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.boardConv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size = 3, padding = 0, stride = 3, bias = True),
            nn.LeakyReLU(),
            nn.Conv2d(32, 64, kernel_size = 3, padding = 0, stride = 3, bias = True),
            nn.LeakyReLU())
        
        self.boardWonConv = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size = 3, padding = 0, stride = 3, bias = True),
            nn.LeakyReLU())
        
        
        self.playableBoardConv = nn.Sequential(nn.Conv2d(1, 64, kernel_size = 3, padding = 0, stride = 3, bias = True),
            nn.LeakyReLU())
        
        self.linearLayer = nn.Sequential(nn.Linear(192, 192),
                            nn.LeakyReLU(),
                            nn.Linear(192, 192),
                            nn.LeakyReLU(),
                            nn.Linear(192, 3),
                            nn.Softmax(dim=1))
                            
        self.flatten = nn.Flatten(1)
         

    def forward(self, input):
        boards = input[0]
        boards = self.boardConv(boards)
        boardsWon = input[1]
        boardsWon = self.boardWonConv(boardsWon) 
        playableBoards = input[2]
        playableBoards = self.playableBoardConv(playableBoards)
        full = self.flatten(torch.stack((boards,boardsWon,playableBoards),dim=1))
        output = self.linearLayer(full)
        return output
    
    def getRotations(tensor):
        return torch.concat((tensor,
                         torch.rot90(tensor,1,(2,3)),
                         torch.rot90(tensor,2,(2,3)),
                         torch.rot90(tensor,3,(2,3)),
                         torch.flip(tensor,(2,)),
                         torch.rot90(torch.flip(tensor,(2,)),1,(2,3)),
                         torch.rot90(torch.flip(tensor,(2,)),2,(2,3)),
                         torch.rot90(torch.flip(tensor,(2,)),3,(2,3))),dim=0)

    def save(self, optimizer, epoch, time, file_name='HeuristicNetwork.pth'):
        model_folder_path = './NeuralNet/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'time': time
            }, file_name)
        
    def fileExists(file_name='HeuristicNetwork.pth'):
        model_file =  f'./NeuralNet/{file_name}'
        return os.path.exists(model_file) 
        
        
    def load_train(file_name='HeuristicNetwork.pth',device = None,adam=True):
        if (device is None):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        model_file =  f'./NeuralNet/{file_name}'
        if not os.path.exists(model_file):
            return None
        checkpoint = torch.load(model_file,map_location=device)
        model = HeuristicNetwork().to(device)
        if (adam):
            optimizer = torch.optim.Adam(model.parameters())
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        else:
            optimizer = torch.optim.SGD(model.parameters())

        model.load_state_dict(checkpoint['model_state_dict'])
        epoch = checkpoint['epoch']
        time = checkpoint['time'] 
        model.train()
        return (model,optimizer,epoch,time)
        
    def load_eval(file_name='HeuristicNetwork.pth', device = None):
        if (device is None):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        model_file =  f'./NeuralNet/{file_name}'
        if not os.path.exists(model_file):
            return None
        model = HeuristicNetwork().to(device)
        checkpoint = torch.load(model_file,map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        return model
    
    def gameToTorch(game):
        board = numpy.array(numpy.zeros(shape=(1,3,9,9),dtype=numpy.float32))
        for b in range(0,9):
            coord = g.GameState.boardToCoord(b)
            for i in range(0,3):
                for j in range(0,3):
                    if (game.board[b,i,j] == game.currentTurn):
                        board[0,0,i+3*coord[0],j+3*coord[1]] = 1
                    elif (game.board[b,i,j] == g.OPEN_VAL):
                        board[0,2,i+3*coord[0],j+3*coord[1]] = 1
                    else:
                        board[0,1,i+3*coord[0],j+3*coord[1]] = 1  
                        
        currentBoard = numpy.array(numpy.zeros(shape=(1,1,3,3),dtype=numpy.float32))
        anyBoard = False
        if (game.currentBoard < 9):
            coord = g.GameState.boardToCoord(game.currentBoard)
            currentBoard[0,0,coord[0],coord[1]] = 1
        else:
            anyBoard = True
        
        boardsWon = numpy.array(numpy.zeros(shape=(1,3,3,3),dtype=numpy.float32))
        for i in range(0,3):
            for j in range(0,3):
                if (game.boardsWon[i,j] == g.OPEN_VAL):
                    if anyBoard:
                        currentBoard[0,0,i,j] = 1
                elif (game.boardsWon[i,j] == game.currentTurn):
                    boardsWon[0,0,i,j] = 1
                elif (game.boardsWon[i,j] == g.STALEMATE):
                    boardsWon[0,2,i,j] = 1
                else:
                    boardsWon[0,1,i,j] = 1
        
        return (torch.tensor(board),
                torch.tensor(boardsWon),
                torch.tensor(currentBoard))
        
    def gameToTorch_dataset(game):
        tensors = HeuristicNetwork.gameToTorch(game)    
            
        return (HeuristicNetwork.getRotations(tensors[0]),
                HeuristicNetwork.getRotations(tensors[1]),
                HeuristicNetwork.getRotations(tensors[2]))
        