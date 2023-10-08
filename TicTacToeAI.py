import GameState as g
import random as r
from abc import ABC, abstractmethod
import copy
import itertools

class TicTacToeAI:
    @abstractmethod
    def chooseMove(game):
       return

    def isWinBoard(game,board,row,column):
        if (game.board[board,row,column] != 0):
            return -2
        game.board[board,row,column] = game.currentTurn
        boardWin = game.isBoardWon(board,row,column)
        game.board[board,row,column] = 0
        return boardWin
    
    def isWinningMove(game,board,row,column):
        boardWon = TicTacToeAI.isWinBoard(game,board,row,column)
        if (boardWon == -2):
            return -2
        elif (boardWon == 0):
            return 0
        tempGame = copy.deepcopy(game)
        tempGame.playTurn(board,row,column)
        return tempGame.gameWon
    
    def canOpponentWinBoard(game,board,row,column):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinBoard(newGame,move[0],move[1],move[2])
            if (boardWin == 1):
                return 1
        return 0

    def canOpponentWin(game,board,row,column):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinningMove(newGame,move[0],move[1],move[2])
            if (boardWin == 1):
                return 1
        return 0
        

class RandomAI(TicTacToeAI): 
    def chooseMove(game):
        possibleMoves = game.getMoves()
        return possibleMoves[r.randrange(len(possibleMoves))]
    
class ChooseWinLose(TicTacToeAI):
    
    def  __init__(self,priority:int):
        self.setPriority(priority)
    
    def setPriority(self,priority):
        p = (0,1,2,3)
        perm = []
        if (priority < 24):
            perm = list(itertools.permutations(p))
            self.priority = copy.deepcopy(perm[priority])
        elif (priority < 64):
            for i in range(1,len(p)):
                perm.extend(list(itertools.permutations(p, r=i)))
            self.priority = copy.deepcopy(perm[priority-24])
        else: # Invalid value - Set to default
            print("Invalid Priority - Setting to default")
            self.priority = copy.deepcopy((0,1,2,3))
    
    def chooseMove(self,game):
        possibleMoves = game.getMoves()
        goodMoves = []
        otherMoves = []
        badMoves = []
        winLoss = [0,0,0,0]
        flag = 0
        for move in possibleMoves:
            flag = 0
            winLoss[0] = ChooseWinLose.isWinningMove(game,move[0],move[1],move[2])
            winLoss[1] = ChooseWinLose.canOpponentWin(game,move[0],move[1],move[2])
            winLoss[2] = ChooseWinLose.isWinBoard(game,move[0],move[1],move[2])
            winLoss[3] = ChooseWinLose.canOpponentWinBoard(game,move[0],move[1],move[2])
            for i in self.priority:
                if (winLoss[i] == 1):
                    if (i % 2 == 0):
                        goodMoves.append(move)
                        flag = 1
                        break
                    else:
                       badMoves.append(move)
                       flag = 1
                       break 
            if (flag == 0):
                otherMoves.append(move)
                
        if (len(goodMoves) > 0):
            return goodMoves[r.randrange(len(goodMoves))]
        elif (len(otherMoves) > 0):
            return otherMoves[r.randrange(len(otherMoves))]
        else:
            return badMoves[r.randrange(len(badMoves))]
            