import GameState as g
import TicTacToeAI as AI
import Heuristics as h

# Pygame UI is based on https://github.com/russs123/TicTacToe/blob/master/tictactoe.py

# IMPORTANT: Run Xlaunch when testing in WSL with Disable Access Control

import pygame
from pygame.locals import *

pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900

BOARD_HEIGHT = SCREEN_HEIGHT // 3
BOARD_WIDTH = SCREEN_WIDTH // 3

GRID_HEIGHT = SCREEN_HEIGHT // 9
GRID_WIDTH = SCREEN_WIDTH // 9

CURRENT_BOARD_X = (255, 220, 220)
CURRENT_BOARD_O = (220, 220, 255)

BACKGROUND_COLOUR = (250,250,250)
GRID_COLOUR = (10,10,10)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ultimate Tic Tac Toe')

GRID_LINE_WIDTH = 3
BOARD_LINE_WIDTH = 9
X_IMAGE = pygame.image.load("X.png")
O_IMAGE = pygame.image.load("O.png")

X_IMAGE_LARGE = pygame.image.load("X_large.png")
O_IMAGE_LARGE = pygame.image.load("O_large.png")

game = g.GameState()

def drawBoard():
    screen.fill(BACKGROUND_COLOUR)
    if game.gameWon == g.NO_WIN:
        drawCurrentBoard()
    for i in range (0,3):
        for j in range(1,3):
            pygame.draw.line(screen,GRID_COLOUR,(0,i*BOARD_HEIGHT+j*GRID_HEIGHT),(SCREEN_WIDTH,i*BOARD_HEIGHT+j*GRID_HEIGHT),GRID_LINE_WIDTH)
            pygame.draw.line(screen,GRID_COLOUR,(i*BOARD_WIDTH+j*(GRID_WIDTH),0),(i*BOARD_WIDTH+j*(GRID_WIDTH),SCREEN_HEIGHT),GRID_LINE_WIDTH)
        if i != 2:
            pygame.draw.line(screen,GRID_COLOUR,(0,(i+1)*BOARD_HEIGHT),(SCREEN_WIDTH,(i+1)*BOARD_HEIGHT),BOARD_LINE_WIDTH)
            pygame.draw.line(screen,GRID_COLOUR,((i+1)*BOARD_WIDTH,0),((i+1)*BOARD_WIDTH,SCREEN_HEIGHT),BOARD_LINE_WIDTH)
            
def drawCurrentBoard():
    currentBoardColour = CURRENT_BOARD_X if game.currentTurn == 1 else CURRENT_BOARD_O
    if game.currentBoard != g.ANYBOARD:
       coord = g.GameState.boardToCoord(game.currentBoard)
       screen.fill(currentBoardColour,(coord[1]*BOARD_WIDTH,coord[0]*BOARD_HEIGHT,BOARD_WIDTH,BOARD_HEIGHT))
    else:
        for i in range(0,3):
            for j in range(0,3):
                if not game.boardsWon[i][j]:
                    screen.fill(currentBoardColour,(j*BOARD_WIDTH,i*BOARD_HEIGHT,BOARD_WIDTH,BOARD_HEIGHT))

def drawMarkerGrid(board, row, column):
    coord = g.GameState.boardToCoord(board)
    screen_x = coord[1]*BOARD_WIDTH + column*GRID_WIDTH
    screen_y = coord[0]*BOARD_HEIGHT + row*GRID_HEIGHT
    if game.board[board,row,column] == g.X_VAL:
        screen.blit(X_IMAGE,(screen_x,screen_y))  
    elif game.board[board,row,column] == g.O_VAL:
        screen.blit(O_IMAGE,(screen_x,screen_y))
        
def drawMarkerBoard(board):
    coord = g.GameState.boardToCoord(board)
    screen_x = (coord[1]*BOARD_WIDTH)
    screen_y = (coord[0]*BOARD_HEIGHT)
    if game.boardsWon[coord[0]][coord[1]] == g.X_VAL:
        screen.blit(X_IMAGE_LARGE,(screen_x,screen_y))
    elif game.boardsWon[coord[0]][coord[1]] == g.O_VAL:
        screen.blit(O_IMAGE_LARGE,(screen_x,screen_y))
    else:
       for i in range(0,3):
            for j in range(0,3):
                if game.board[board,i,j]:
                    drawMarkerGrid(board,i,j)              

        
def drawMarkers():
    for b in range(0,9):
        drawMarkerBoard(b)
        
def updateDraw():
    drawBoard()
    drawMarkers()
    pygame.display.update()

drawBoard()
pygame.display.update()

click = False
mousePosition = []


# Run until user quits
run = True 

AIPlayer = AI.MonteCarloST(1000,threads=2)
#AIPlayer = AI.ChooseMinimax(7,h.PlayableBoardHeuristic())

while run:  
    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and click == False:
            click = True
        if event.type == pygame.MOUSEBUTTONUP and click:
            click = False
            
            # Find click position
            mousePosition = pygame.mouse.get_pos()
            x = mousePosition[0]
            y = mousePosition[1]
            
            # Find clicked board
            boardRow = 3*y // SCREEN_HEIGHT
            boardColumn = 3*x // SCREEN_WIDTH
            board = g.GameState.coordToBoard(boardRow,boardColumn)

            #Find clicked grid
            if game.gameWon == 0:# and game.currentTurn == 1:
                gridRow = 9*(y % BOARD_HEIGHT) // SCREEN_HEIGHT
                gridColumn = 9*(x % BOARD_HEIGHT) // SCREEN_WIDTH 
                
                move = game.playTurn(board,gridRow,gridColumn)

                if move != -1:         
                    updateDraw()
                    
    if game.gameWon == 0 and game.currentTurn == 2:
        
        moveAI = AIPlayer.chooseMove(game)
        move = game.playTurn(moveAI[0],moveAI[1],moveAI[2])
        if move != -1:                    
            updateDraw()
    
            
            
        
        
pygame.quit()