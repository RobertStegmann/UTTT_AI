import numpy

class GameState:
    
    def   __init__(self):
        self.board = numpy.array(numpy.zeros(shape=(9,3,3),dtype=numpy.int8))
        self.boardsWon = numpy.array(numpy.zeros(shape=(3,3),dtype=numpy.int8))
        self.currentBoard = 9
        self.currentTurn = 1 # 1 is player 1, 2 is player 2
        self.gameWon = 0 # 0: game not won, 1 game is won, -1 stalemate   

    def playTurn(self,board: int,row: int,column: int):
        if self.isValidMove(board,row,column): # If move is legal
            self.board[board,row,column] = self.currentTurn # Update board
            boardWin = self.isBoardWon(board,row,column)
            if boardWin == 1 : # Check if board is won
                coord = GameState.boardToCoord(board)
                self.boardsWon[coord[0],coord[1]] = self.currentTurn
                self.gameWon = self.isGameWon(board)
                if self.gameWon: # Check if game is over
                    return self.gameWon
            elif boardWin == -1:
                coord = GameState.boardToCoord(board)
                self.boardsWon[coord[0],coord[1]] = -1
                self.gameWon = self.isGameWon(board)
                if self.gameWon: # Check if game is over
                    return self.gameWon
            
            if self.currentTurn == 1: # If the turn is player 1
                self.currentTurn = 2
            else: # If the turn is player 2
                self.currentTurn = 1   
            
            # Set next board    
            if self.boardsWon[row, column] == 0: 
                self.currentBoard = row * 3 + column
            else:
                self.currentBoard = 9       
            return 0    
        else: # If move is illegal
            return -1    
    
    def isValidMove(self,board: int,row: int,column: int):
        if  board == self.currentBoard or self.currentBoard == 9:        
            if self.board[board,row,column]:
                return False
            coord = GameState.boardToCoord(board)
            if self.boardsWon[coord[0],coord[1]]:
                return False
            else:
                return True
        else:
            return False
    
    def isBoardWon(self,board: int,row: int,column: int):
        if self.board[board,row,0] == self.board[board,row,1] and self.board[board,row,1] == self.board[board,row,2]:
            return 1
        elif self.board[board,0,column] == self.board[board,1,column] and self.board[board,1,column] == self.board[board,2,column]:
            return 1
        elif row == column and self.board[board,0,0] == self.board[board,1,1] and self.board[board,1,1] == self.board[board,2,2]:
            return 1
        elif (row + column) == 2 and self.board[board,0,2] == self.board[board,1,1] and self.board[board,1,1] == self.board[board,2,0]:
            return 1
        else:
            for i in range(0,3):
                for j in range(0,3):
                    if self.board[board,i,j] == 0:
                        return 0
            return -1
            
    def isGameWon(self,board):
        coord = GameState.boardToCoord(board)
        boardRow = coord[0]
        boardColumn = coord[1]
        if self.boardsWon[boardRow,0] == self.boardsWon[boardRow,1] and self.boardsWon[boardRow,1] == self.boardsWon[boardRow ,2]:
            return 1
        elif self.boardsWon[0,boardColumn] == self.boardsWon[1,boardColumn] and self.boardsWon[1,boardColumn] == self.boardsWon[2,boardColumn]:
            return 1
        elif boardRow == boardColumn and self.boardsWon[0,0] == self.boardsWon[1,1] and self.boardsWon[1,1] == self.boardsWon[2,2]:
            return 1
        elif (boardRow + boardColumn) == 2 and self.boardsWon[0,2] == self.boardsWon[1,1] and self.boardsWon[1,1] == self.boardsWon[2,0]:
            return 1
        else:
            for i in range(0,3):
                for j in range(0,3):
                    if self.boardsWon[i,j] == 0:
                        return 0
            return -1
    
    def coordToBoard(row,column):
        return row * 3 + column
    
    def boardToCoord (board):
        coord = numpy.array([0,0],dtype=numpy.int8)
        coord[0] = board // 3
        coord[1] = board % 3
        return coord
    
    def chooseMoveFullBoard(self):
        possibleMoves = []
        for b in range(0,9):
            coord = GameState.boardToCoord(b)
            if not self.boardsWon[coord[0]][coord[1]]:
                for i in range(0,3):
                    for j in range(0,3):
                        if not self.board[b][i][j]:
                            possibleMoves.append((b,i,j))
        return possibleMoves
    
    def chooseMoveSingleGrid(self):
        possibleMoves = []
        for i in range(0,3):
            for j in range(0,3):
                if not self.board[self.currentBoard][i][j]:
                    possibleMoves.append((self.currentBoard,i,j))
        return possibleMoves      
    
    def getMoves(self):
        if self.currentBoard == 9:
            possibleMoves = self.chooseMoveFullBoard()
        else:
            possibleMoves = self.chooseMoveSingleGrid()
        return possibleMoves
                
            

        
            