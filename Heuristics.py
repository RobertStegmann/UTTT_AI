import GameState as g
import ctypes
from abc import ABC, abstractmethod

BOARD_VALUE = 140
GRID_VALUE = 10
PLAYABLE_VAL = 16
MAX_RUNS = 100

class HeuristicVal(ctypes.Structure):
    _fields_ = [("boardVal",ctypes.c_int),
                ("gridVal",ctypes.c_int),
                ("playableVal",ctypes.c_int),
                ("maxRuns",ctypes.c_int),
                ("index",ctypes.c_int)]

class Heuristic:
    
    def  __init__(self,*,boardVal = BOARD_VALUE, gridVal = GRID_VALUE,playableVal = PLAYABLE_VAL,maxRuns = MAX_RUNS):
        index = -1
        self.values = HeuristicVal(boardVal,gridVal,playableVal,maxRuns,index)
    
    @abstractmethod
    def Heuristic(self,game: g.GameState):
        return
   
    @abstractmethod
    def toString(self):
        return ""
    
    @abstractmethod
    def valToString(self):
        return ("Board Value: " + str(self.values.boardVal) + 
                " Grid Value: " +  str(self.values.gridVal) +
                " Playable Value: " +  str(self.values.playableVal) +
                " Max Runs: " +  str(self.values.maxRuns))
    
    def evaluateBoard(self,game:g.GameState):
        evaluation = 0
        
        # Rows
        for i in range(0,3):
            xCount = 0
            oCount = 0
            stalemateCount = 0
            for j in range(0,3):
                if game.boardsWon[i,j] == g.X_VAL:
                    xCount = xCount + 1
                elif game.boardsWon[i,j] == g.O_VAL:
                    oCount = oCount + 1
                elif game.boardsWon[i,j] == g.STALEMATE:
                    stalemateCount = stalemateCount + 1
                    
            if oCount == 0 and stalemateCount == 0:
                evaluation += BOARD_VALUE*xCount*xCount
            elif xCount == 0 and stalemateCount == 0:
                evaluation -= BOARD_VALUE*oCount*oCount
        
        # Columns
        for i in range(0,3):
            xCount = 0
            oCount = 0
            stalemateCount = 0
            for j in range(0,3):
                if game.boardsWon[j,i] == g.X_VAL:
                    xCount = xCount + 1
                elif game.boardsWon[j,i] == g.O_VAL:
                    oCount = oCount + 1
                elif game.boardsWon[j,i] == g.STALEMATE:
                    stalemateCount = stalemateCount + 1
            
            if oCount == 0 and stalemateCount == 0:                
                evaluation += BOARD_VALUE*xCount*xCount
            elif xCount == 0 and stalemateCount == 0:
                evaluation -= BOARD_VALUE*oCount*oCount        
    
        xCount = 0
        oCount = 0
        stalemateCount = 0
        for i in range(0,3):
            if game.boardsWon[i,i] == g.X_VAL:
                xCount += 1
            elif game.boardsWon[i,i] == g.O_VAL:
                oCount += 1
            elif game.boardsWon[i,i] == g.STALEMATE:
                stalemateCount += 1
        
        if oCount == 0 and stalemateCount == 0:
            evaluation += BOARD_VALUE*xCount*xCount
        elif xCount == 0 and stalemateCount == 0:
            evaluation -= BOARD_VALUE*oCount*oCount
            
        xCount = 0
        oCount = 0
        stalemateCount = 0
        a = 2
        for i in range(0,3):
            if game.boardsWon[a,i] == g.X_VAL:
                xCount += 1
            elif game.boardsWon[a,i] == g.O_VAL:
                oCount += 1
            elif game.boardsWon[a,i] == g.STALEMATE:
                stalemateCount += 1
            a -= 1
        
        if oCount == 0 and stalemateCount == 0:
            evaluation += BOARD_VALUE*xCount*xCount
        elif xCount == 0 and stalemateCount == 0:
            evaluation -= BOARD_VALUE*oCount*oCount      
                
        return evaluation
    
    def evaluateGrid(self,game:g.GameState,grid:int):
        evaluation = 0
        # Rows
        for i in range(0,3):
            xCount = 0
            oCount = 0
            for j in range(0,3):
                if game.board[grid,i,j] == g.X_VAL:
                    xCount += 1
                elif game.board[grid,i,j] == g.O_VAL:
                    oCount += 1
                    
            if oCount == 0:
                evaluation += GRID_VALUE*xCount*xCount
            elif xCount == 0:
                evaluation -= GRID_VALUE*oCount*oCount
        
        # Columns
        for i in range(0,3):
            xCount = 0
            oCount = 0
            for j in range(0,3):
                if game.board[grid,j,i] == g.X_VAL:
                    xCount += 1
                elif game.board[grid,j,i] == g.O_VAL:
                    oCount+= 1
            
            if oCount == 0:                
                evaluation += GRID_VALUE*xCount*xCount
            elif xCount == 0:
                evaluation -= GRID_VALUE*oCount*oCount        
    
        xCount = 0
        oCount = 0
        for i in range(0,3):
            if game.board[grid,i,i] == g.X_VAL:
                xCount += 1
            elif game.board[grid,i,i] == g.O_VAL:
                oCount += 1
        
        if oCount == 0:
            evaluation += GRID_VALUE*xCount*xCount
        elif xCount == 0:
            evaluation -= GRID_VALUE*oCount*oCount
            
        xCount = 0
        oCount = 0
        a = 2
        for i in range(0,3):
            if game.board[grid,a,i] == g.X_VAL:
                xCount += 1
            elif game.board[grid,a,i] == g.O_VAL:
                oCount += 1
            a -= 1
        
        if oCount == 0:
            evaluation += GRID_VALUE*xCount*xCount
        elif xCount == 0:
            evaluation -= GRID_VALUE*oCount*oCount      
                
        return evaluation
    
class StaticHeuristic(Heuristic):
    
    def  __init__(self,*,boardVal = BOARD_VALUE, gridVal = GRID_VALUE,playableVal = PLAYABLE_VAL,maxRuns = MAX_RUNS):
        index = 1
        self.values = HeuristicVal(boardVal,gridVal,playableVal,maxRuns,index)
    
    def heuristic(self,game:g.GameState):
        evaluation = self.evaluateBoard(game)
        
        for grid in range(0,9):
            coord = g.GameState.boardToCoord(grid)
            if game.boardsWon[coord[0],coord[1]] == g.OPEN_VAL:
                gridEval = self.evaluateGrid(game,grid)
                # Rows
                if coord[1] == 0:
                    otherColumns = (1,2)
                elif coord[1] == 1:
                    otherColumns = (0,2)
                else: 
                    otherColumns = (0,1)
                
                xCount = 0
                oCount = 0
                stalemateCount = 0
                for i in range(0,2):
                    if game.boardsWon[coord[0],otherColumns[i]] == g.X_VAL:
                        xCount += 1
                    elif game.boardsWon[coord[0],otherColumns[i]] == 2:
                        oCount += 1
                    elif game.boardsWon[coord[0],otherColumns[i]] == g.STALEMATE:
                        stalemateCount += 1
                
                if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                    evaluation += gridEval
                
                # Columns
                if coord[0] == 0:
                    otherRows = (1,2)
                elif coord[0] == 1:
                    otherRows = (0,2)
                else: 
                    otherRows = (0,1)
                
                xCount = 0
                oCount = 0
                stalemateCount = 0
                for i in range(0,2):
                    if game.boardsWon[otherRows[i],coord[1]] == g.X_VAL:
                        xCount += 1
                    elif game.boardsWon[otherRows[i],coord[1]] == g.O_VAL:
                        oCount += 1
                    elif game.boardsWon[otherRows[i],coord[1]] == g.STALEMATE:
                        stalemateCount += 1
                
                if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                    evaluation += gridEval
                    
                if coord[0] == coord[1]:
                    if coord[0] == 0:
                        upperLeftDiagonal = (1,2)
                    elif coord[0] == 1:
                        upperLeftDiagonal = (0,2)
                    else: 
                        upperLeftDiagonal = (0,1)
                    
                    xCount = 0
                    oCount = 0
                    stalemateCount = 0
                    for i in upperLeftDiagonal:
                        if game.boardsWon[i,i] == g.X_VAL:
                            xCount += 1
                        elif game.boardsWon[i,i] == g.O_VAL:
                            oCount += 1
                        elif game.boardsWon[i,i] == g.STALEMATE:
                            stalemateCount += 1
                    
                    if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                        evaluation += gridEval  
                  
                if (coord[0] + coord[1]) == 2:
                    if coord[0] == 0:
                        upperRightDiagonal = ((1,1),(2,0))
                    elif coord[0] == 1:
                        upperRightDiagonal = ((0,2),(2,0))
                    else: 
                        upperRightDiagonal = ((0,2),(1,1))
                       
                    xCount = 0
                    oCount = 0
                    stalemateCount = 0

                    for coordTuple in upperRightDiagonal:
                        if game.boardsWon[coordTuple[0],coordTuple[1]] == g.X_VAL:
                            xCount += 1
                        elif game.boardsWon[coordTuple[0],coordTuple[1]] == g.O_VAL:
                            oCount += 1
                        elif game.boardsWon[coordTuple[0],coordTuple[1]] == g.STALEMATE:
                            stalemateCount += 1
                    
                    if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                        evaluation += gridEval  
                        
        return evaluation
   
    def toString(self):
        return "StaticHeuristic\n" + self.valToString()
    
    def valToString(self):
        return ("Board Value: " + str(self.values.boardVal) + 
                " Grid Value: " +  str(self.values.gridVal)) 

class StaticHeuristicC(Heuristic):    
    
    def  __init__(self,*,boardVal = BOARD_VALUE, gridVal = GRID_VALUE,playableVal = PLAYABLE_VAL,maxRuns = MAX_RUNS):
        index = 0
        self.values = HeuristicVal(boardVal,gridVal,playableVal,maxRuns,index)
    
    def heuristic(self,game:g.GameState):
        return g.clibrary.staticHeuristicWrapper(game.toCGameState(),self.values)
   
    def toString(self):
        return "StaticHeuristic using C\n" + self.valToString()
    
    def valToString(self):
        return ("Board Value: " + str(self.values.boardVal) + 
                " Grid Value: " +  str(self.values.gridVal)) 
    
class PlayableBoardHeuristic(Heuristic):
    
    def  __init__(self,*,boardVal = BOARD_VALUE, gridVal = GRID_VALUE,playableVal = PLAYABLE_VAL,maxRuns = MAX_RUNS):
        index = 1
        self.values = HeuristicVal(boardVal,gridVal,playableVal,maxRuns,index)
    
    def heuristic(self,game:g.GameState):
        return g.clibrary.playableBoardHeuristicWrapper(game.toCGameState(),self.values)
   
    def toString(self):
        return "PlayableBoardHeuristic\n" + self.valToString()
    
    def valToString(self):
        return ("Board Value: " + str(self.values.boardVal) + 
                " Grid Value: " +  str(self.values.gridVal) +
                " Playable Value: " +  str(self.values.playableVal))
        
class MonteCarloHeuristic(Heuristic):
    
    def  __init__(self,*,boardVal = BOARD_VALUE, gridVal = GRID_VALUE,playableVal = PLAYABLE_VAL,maxRuns = MAX_RUNS):
        index = 2
        self.values = HeuristicVal(boardVal,gridVal,playableVal,maxRuns,index)
    
    def heuristic(self,game:g.GameState):
        return g.clibrary.monteCarloHeuristicWrapper(game.toCGameState(),self.values)
   
    def toString(self):
        return "MonteCarloHeuristic: " + self.valToString()
    
    def valToString(self):
        return ("# of Runs: " + str(self.values.maxRuns))

    
    