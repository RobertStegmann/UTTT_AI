import GameState as g
import random as r
from abc import ABC, abstractmethod
import copy
import itertools

class TicTacToeAI:
    @abstractmethod
    def chooseMove(self,game: g.GameState):
       return
   
    @abstractmethod
    def toString(self):
        return "TicTacToeAI"

    def isWinBoard(game: g.GameState,board: int,row: int,column: int):
        if (game.board[board,row,column] != 0):
            return -2
        game.board[board,row,column] = game.currentTurn
        boardWin = game.isBoardWon(board,row,column)
        game.board[board,row,column] = 0
        return boardWin
    
    def isWinningMove(game: g.GameState,board: int,row: int,column: int):
        boardWon = TicTacToeAI.isWinBoard(game,board,row,column)
        if (boardWon == -2):
            return -2
        elif (boardWon == 0):
            return 0
        tempGame = copy.deepcopy(game)
        tempGame.playTurn(board,row,column)
        return tempGame.gameWon
    
    def canOpponentWinBoard(game: g.GameState,board: int,row: int,column: int):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinBoard(newGame,move[0],move[1],move[2])
            if (boardWin == 1):
                return 1
        return 0

    def canOpponentWin(game: g.GameState,board: int,row: int,column: int):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinningMove(newGame,move[0],move[1],move[2])
            if (boardWin == 1):
                return 1
        return 0
        

class RandomAI(TicTacToeAI): 
    def chooseMove(self,game: g.GameState):
        possibleMoves = game.getMoves()
        return possibleMoves[r.randrange(len(possibleMoves))]
    
    def toString(self):
        return "RandomAI"
    
class ChooseWinLose(TicTacToeAI):
    
    def  __init__(self,priority:int):
        self.setPriority(priority)
    
    def toString(self):
        string = "ChooseWinLose:"
        count = 1
        for i in self.priority:
            if (i == 0):
                string = string + " Win Game"
            elif (i == 1):
                string = string + " Don't Lose"
            elif (i == 2):
                string = string + " Win Board"
            elif (i == 3):
                string = string + " Don't Lose Board"
            if (count != len(self.priority)):
                string = string + ","
            count = count + 1
        return string
        
        
    def setPriority(self,priority: int):
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
    
    def chooseMove(self,game: g.GameState):
        possibleMoves = game.getMoves()
        winningMoves = []
        goodMoves = []
        otherMoves = []
        badMoves = []
        losingMoves = []
        winLoss = [0,0,0,0]
        flag = 0
        for move in possibleMoves:
            flag = 0
            if 0 in self.priority:
                winLoss[0] = ChooseWinLose.isWinningMove(game,move[0],move[1],move[2])
            if 1 in self.priority:   
                winLoss[1] = ChooseWinLose.canOpponentWin(game,move[0],move[1],move[2])
            if 2 in self.priority:
                winLoss[2] = ChooseWinLose.isWinBoard(game,move[0],move[1],move[2])
            if 3 in self.priority:
                winLoss[3] = ChooseWinLose.canOpponentWinBoard(game,move[0],move[1],move[2])
            for i in self.priority:
                if (winLoss[i] == 1):
                    if (i == 0):
                        winningMoves.append(move)
                        flag = 1
                        break
                    elif (i == 1):
                        losingMoves.append(move)
                        flag = 1
                        break
                    elif (i == 2):
                        goodMoves.append(move)
                        flag = 1
                        break
                    else:
                       badMoves.append(move)
                       flag = 1
                       break 
            if (flag == 0):
                otherMoves.append(move)
        if (len(winningMoves) > 0):
            return winningMoves[r.randrange(len(winningMoves))]        
        elif (len(goodMoves) > 0):
            return goodMoves[r.randrange(len(goodMoves))]
        elif (len(otherMoves) > 0):
            return otherMoves[r.randrange(len(otherMoves))]
        elif (len(badMoves) > 0):
            return badMoves[r.randrange(len(badMoves))]
        else:
            return losingMoves[r.randrange(len(losingMoves))]
            