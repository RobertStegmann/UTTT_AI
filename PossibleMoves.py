import GameState as g
import RandomAI as r
import copy
import time

boardCount = 0

def countMoves(game):
    if game.currentBoard == 9:
        possibleMoves = game.chooseMoveFullBoard()
    else:
        possibleMoves = game.chooseMoveSingleGrid()
    for move in possibleMoves:
        newGame = copy.deepcopy(game)
        newGame.playTurn(move[0],move[1],move[2])
        global boardCount 
        boardCount += 1
        if not newGame.gameWon:
            countMoves(newGame)

start = time.time()

# Top Left corner

for i in range(0,3):
    for j in range (0,(i+1)):
        startingBoard = g.GameState()
        startingBoard.playTurn(0,i,j)
        countMoves(startingBoard)
        print("Possible moves from starting at 0," + i + "," + j + ":" + boardCount)
        boardCount = 0
        
# Top Centre
        
for i in range(0,3):
    for j in range (0,2):
        startingBoard = g.GameState()
        startingBoard.playTurn(0,i,j)
        countMoves(startingBoard)
        print("Possible moves from starting at 1," + i + "," + j + ":" + boardCount)
        boardCount = 0       

# Centre

startingBoard = g.GameState()
startingBoard.playTurn(0,0,0)
countMoves(startingBoard)
print("Possible moves from starting at 5,0,0:" + boardCount)
boardCount = 0

startingBoard = g.GameState()
startingBoard.playTurn(0,0,1)
countMoves(startingBoard)
print("Possible moves from starting at 5,0,1:" + boardCount)
boardCount = 0   

startingBoard = g.GameState()
startingBoard.playTurn(0,1,1)
countMoves(startingBoard)
print("Possible moves from starting at 5,1,1:" + boardCount)
boardCount = 0

end = time.time()
print(end - start)







