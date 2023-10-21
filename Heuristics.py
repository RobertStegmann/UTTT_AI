import GameState as g
from abc import ABC, abstractmethod

BOARD_VALUE = 20
GRID_VALUE = 1

class Heuristic:
    @abstractmethod
    def Heuristic(self,game: g.GameState):
       return
   
    @abstractmethod
    def toString(self):
        return ""
    
    def evaluateBoard(self,game:g.GameState):
        evaluation = 0
        
        # Rows
        for i in range(0,3):
            xCount = 0
            oCount = 0
            stalemateCount = 0
            for j in range(0,3):
                if game.boardsWon[i,j] == 1:
                    xCount = xCount + 1
                elif game.boardsWon[i,j] == 2:
                    oCount = oCount + 1
                elif game.boardsWon[i,j] == -1:
                    stalemateCount = stalemateCount + 1
                    
            if oCount == 0 and stalemateCount == 0:
                evaluation = evaluation + BOARD_VALUE*xCount*xCount
            elif xCount == 0 and stalemateCount == 0:
                evaluation = evaluation - BOARD_VALUE*oCount*oCount
        
        # Columns
        for i in range(0,3):
            xCount = 0
            oCount = 0
            stalemateCount = 0
            for j in range(0,3):
                if game.boardsWon[j,i] == 1:
                    xCount = xCount + 1
                elif game.boardsWon[j,i] == 2:
                    oCount = oCount + 1
                elif game.boardsWon[j,i] == -1:
                    stalemateCount = stalemateCount + 1
            
            if oCount == 0 and stalemateCount == 0:                
                evaluation = evaluation + BOARD_VALUE*xCount*xCount
            elif xCount == 0 and stalemateCount == 0:
                evaluation = evaluation - BOARD_VALUE*oCount*oCount        
    
        xCount = 0
        oCount = 0
        stalemateCount = 0
        for i in range(0,3):
            if game.boardsWon[i,i] == 1:
                xCount = xCount + 1
            elif game.boardsWon[i,i] == 2:
                oCount = oCount + 1
            elif game.boardsWon[i,i] == -1:
                stalemateCount = stalemateCount + 1
        
        if oCount == 0 and stalemateCount == 0:
            evaluation = evaluation + BOARD_VALUE*xCount*xCount
        elif xCount == 0 and stalemateCount == 0:
            evaluation = evaluation - BOARD_VALUE*oCount*oCount
            
        xCount = 0
        oCount = 0
        stalemateCount = 0
        a = 2
        for i in range(0,3):
            if game.boardsWon[a,i] == 1:
                xCount = xCount + 1
            elif game.boardsWon[a,i] == 2:
                oCount = oCount + 1
            elif game.boardsWon[a,i] == -1:
                stalemateCount = stalemateCount + 1
            a = a - 1
        
        if oCount == 0 and stalemateCount == 0:
            evaluation = evaluation + BOARD_VALUE*xCount*xCount
        elif xCount == 0 and stalemateCount == 0:
            evaluation = evaluation - BOARD_VALUE*oCount*oCount      
                
        return evaluation
    
    def evaluateGrid(self,game:g.GameState,grid:int):
        evaluation = 0
        # Rows
        for i in range(0,3):
            xCount = 0
            oCount = 0
            for j in range(0,3):
                if game.board[grid,i,j] == 1:
                    xCount = xCount + 1
                elif game.board[grid,i,j] == 2:
                    oCount = oCount + 1
                    
            if oCount == 0:
                evaluation = evaluation + GRID_VALUE*xCount*xCount
            elif xCount == 0:
                evaluation = evaluation - GRID_VALUE*oCount*oCount
        
        # Columns
        for i in range(0,3):
            xCount = 0
            oCount = 0
            for j in range(0,3):
                if game.board[grid,j,i] == 1:
                    xCount = xCount + 1
                elif game.board[grid,j,i] == 2:
                    oCount = oCount + 1
            
            if oCount == 0:                
                evaluation = evaluation + GRID_VALUE*xCount*xCount
            elif xCount == 0:
                evaluation = evaluation - GRID_VALUE*oCount*oCount        
    
        xCount = 0
        oCount = 0
        for i in range(0,3):
            if game.board[grid,i,i] == 1:
                xCount = xCount + 1
            elif game.board[grid,i,i] == 2:
                oCount = oCount + 1
        
        if oCount == 0:
            evaluation = evaluation + GRID_VALUE*xCount*xCount
        elif xCount == 0:
            evaluation = evaluation - GRID_VALUE*oCount*oCount
            
        xCount = 0
        oCount = 0
        a = 2
        for i in range(0,3):
            if game.board[grid,a,i] == 1:
                xCount = xCount + 1
            elif game.board[grid,a,i] == 2:
                oCount = oCount + 1
            a = a - 1
        
        if oCount == 0:
            evaluation = evaluation + GRID_VALUE*xCount*xCount
        elif xCount == 0:
            evaluation = evaluation - GRID_VALUE*oCount*oCount      
                
        return evaluation
    
class StaticHeuristic(Heuristic):
    def heuristic(self,game:g.GameState):
        evaluation = self.evaluateBoard(game)
        
        for i in range(0,9):
            coord = g.GameState.boardToCoord(i)
            if game.boardsWon[coord[0],coord[1]] == 0:
                gridEval = self.evaluateGrid(game,i)
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
                    if game.boardsWon[coord[0],otherColumns[i]] == 1:
                        xCount = xCount + 1
                    elif game.boardsWon[coord[0],otherColumns[i]] == 2:
                        oCount = oCount + 1
                    elif game.boardsWon[coord[0],otherColumns[i]] == -1:
                        stalemateCount = stalemateCount + 1
                
                if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                    evaluation = evaluation + gridEval
                
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
                    if game.boardsWon[otherRows[i],coord[1]] == 1:
                        xCount = xCount + 1
                    elif game.boardsWon[otherRows[i],coord[1]] == 2:
                        oCount = oCount + 1
                    elif game.boardsWon[otherRows[i],coord[1]] == -1:
                        stalemateCount = stalemateCount + 1
                
                if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                    evaluation = evaluation + gridEval
                    
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
                        if game.boardsWon[i,i] == 1:
                            xCount = xCount + 1
                        elif game.boardsWon[i,i] == 2:
                            oCount = oCount + 1
                        elif game.boardsWon[i,i] == -1:
                            stalemateCount = stalemateCount + 1
                    
                    if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                        evaluation = evaluation + gridEval  
                  
                if (coord[0] + coord[1]) == 2:
                    if coord[0] == 0:
                        upperRightDiagonal = ((1,1),(2,0))
                    elif coord[0] == 1:
                        upperRightDiagonal  = ((0,2),(2,0))
                    else: 
                        upperRightDiagonal  = ((0,2),(1,1))
                       
                    xCount = 0
                    oCount = 0
                    stalemateCount = 0

                    for coordTuple in upperRightDiagonal:
                        if game.boardsWon[coordTuple[0],coordTuple[1]] == 1:
                            xCount = xCount + 1
                        elif game.boardsWon[coordTuple[0],coordTuple[1]] == 2:
                            oCount = oCount + 1
                        elif game.boardsWon[coordTuple[0],coordTuple[1]] == -1:
                            stalemateCount = stalemateCount + 1
                    
                    if stalemateCount == 0 and (xCount == 0 or oCount == 0):
                        evaluation = evaluation + gridEval  
                        
        return evaluation
   
    def toString(self):
        return "StaticHeuristic"