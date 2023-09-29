#ifndef _BOARDCOUNT_H
#define _BOARDCOUNT_H

#include <pthread.h>     /* pthreads library */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 
#include <time.h>
#include <string.h> 

#define BOARDSIZE 81
#define GRIDSIZE 9

#define ANYBOARD 9

#define X_VAL 1
#define O_VAL 2

#define OPEN_VAL 0
#define STALEMATE -1
#define GAME_WON 1
#define NO_WIN 0
#define ROW_DIMENSION 3
#define COL_DIMENSION ROW_DIMENSION

typedef struct {
    char *** board;
    char ** boardsWon;
    unsigned char currentBoard;
    unsigned char currentTurn;
    char gameWon;
} GameState;

typedef struct {
    unsigned char board;
    unsigned char row;
    unsigned char column;
} Coord;

typedef struct {
    int layers;
    Coord coords;
} Args;

void * countTopLeft(void * foo);
void * countTopCentre(void * foo);
void * countCentre(void * foo);
void * countFromStartWrapper(void * arg);
void * countFromStartWrapperLayers(void * arg);
void countFromStart(int board, int row, int column);
void countFromStartLayers(int board, int row, int column, int layers);

void * countTopLeftLayers(void * mLayers);
void * countTopCentreLayers(void * mLayers);
void * countCentreLayers(void * mLayers);

GameState * createGameState();
GameState * cloneGameState(GameState * game);
void freeGameState(GameState * game);
int isValidMove(GameState * game, int board, int row, int column);
int isBoardWon (GameState * game, int board, int row, int column);
int isGameWon(GameState * game, int board);
int playTurn(GameState * game, int board, int row, int column);
double countMoves(GameState *game);
double countMovesLayers(GameState *game, int layers);
Coord *chooseMoveFullBoard(GameState *game);
Coord *chooseMoveSingleGrid(GameState *game, unsigned char board);

#endif