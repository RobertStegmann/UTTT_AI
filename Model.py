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
        
        self.linearLayer = nn.Sequential(nn.Linear(1024, 1024),
                            nn.LeakyReLU(),
                            nn.Linear(1024, 1024),
                            nn.LeakyReLU(),
                            nn.Linear(1024, 3),
                            nn.Softmax(dim=0))
                            
        self.flatten = nn.Flatten(0)
         

    def forward(self, input):
        boards = HeuristicNetwork.getRotations(input[0])
        boards = self.boardConv(boards)
        boardsWon = HeuristicNetwork.getRotations(input[1])
        boardsWon = self.boardWonConv(boardsWon)        
        playableBoards = HeuristicNetwork.getRotations(input[2])
        playableBoards = self.playableBoardConv(playableBoards)
        
        full = self.flatten(torch.stack((boards,boardsWon)))
         
        output = self.linearLayer(full)
        return output
    
    def getRotations(tensor):
        return torch.stack((tensor,
                         torch.rot90(tensor,1,(1,2)),
                         torch.rot90(tensor,2,(1,2)),
                         torch.rot90(tensor,3,(1,2)),
                         torch.flip(tensor,(1,)),
                         torch.rot90(torch.flip(tensor,(1,)),1,(1,2)),
                         torch.rot90(torch.flip(tensor,(1,)),2,(1,2)),
                         torch.rot90(torch.flip(tensor,(1,)),3,(1,2))))

    def save(self, optimizer, epoch, file_name='HeuristicNetwork.pth'):
        model_folder_path = './NeuralNet/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            }, file_name)
        
    def fileExists(file_name='HeuristicNetwork.pth'):
        model_file =  f'./NeuralNet/{file_name}'
        return os.path.exists(model_file) 
        
        
    def load_train(file_name='HeuristicNetwork.pth'):
        model_file =  f'./NeuralNet/{file_name}'
        if not os.path.exists(model_file):
            return None
        checkpoint = torch.load(model_file)
        model = HeuristicNetwork()
        optimizer = torch.optim.Adam(model.parameters())
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        model.train()
        return (model,optimizer,epoch)
        
    def load_eval(file_name='HeuristicNetwork.pth'):
        model_file =  f'./NeuralNet/{file_name}'
        if not os.path.exists(model_file):
            return None
        model = HeuristicNetwork()
        checkpoint = torch.load(model_file)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        return model
    
    def gameToTorch(game):
        board = numpy.array(numpy.zeros(shape=(3,9,9),dtype=numpy.float32))
        for b in range(0,9):
            coord = g.GameState.boardToCoord(b)
            for i in range(0,3):
                for j in range(0,3):
                    if (game.board[b,i,j] == game.currentTurn):
                        board[0,i+3*coord[0],j+3*coord[1]] = 1
                    elif (game.board[b,i,j] == g.OPEN_VAL):
                        board[2,i+3*coord[0],j+3*coord[1]] = 1
                    else:
                        board[1,i+3*coord[0],j+3*coord[1]] = 1  
                        
        currentBoard = numpy.array(numpy.zeros(shape=(1,3,3),dtype=numpy.float32))
        anyBoard = False
        if (game.currentBoard < 9):
            coord = g.GameState.boardToCoord(game.currentBoard)
            currentBoard[0,coord[0],coord[1]] = 1
        else:
            anyBoard = True
        
        boardsWon = numpy.array(numpy.zeros(shape=(3,3,3),dtype=numpy.float32))
        for i in range(0,3):
            for j in range(0,3):
                if (game.boardsWon[i,j] == g.OPEN_VAL):
                    if anyBoard:
                        currentBoard[0,i,j] = 1
                elif (game.boardsWon[i,j] == game.currentTurn):
                    boardsWon[0,i,j] = 1
                elif (game.boardsWon[i,j] == g.STALEMATE):
                    boardsWon[2,i,j] = 1
                else:
                    boardsWon[1,i,j] = 1
        
        return (torch.tensor(board),torch.tensor(boardsWon),torch.tensor(currentBoard))
        
        
        
        
        
    
    
