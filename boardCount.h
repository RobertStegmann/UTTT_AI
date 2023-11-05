#ifndef _BOARDCOUNT_H
#define _BOARDCOUNT_H

#include <pthread.h>     /* pthreads library */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 
#include <time.h>
#include <string.h> 
#include <stdbool.h>

#define BOARDSIZE 81
#define GRIDSIZE 9

#define ANYBOARD 9

#define X_VAL 1
#define O_VAL 2

#define OPEN_VAL 0
#define STALEMATE 3
#define GAME_WON 1
#define NO_WIN 0
#define ROW_DIMENSION 3
#define COL_DIMENSION ROW_DIMENSION
#define VICTORY_VALUE 10000

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))
#define MAX(X, Y) (((X) > (Y)) ? (X) : (Y))

typedef struct {
    char board[9][ROW_DIMENSION][COL_DIMENSION];
    char boardsWon[ROW_DIMENSION][COL_DIMENSION];
    unsigned char currentBoard;
    unsigned char currentTurn;
    char gameWon;
} CGameState;

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

CGameState * createCGameState();
CGameState * cloneCGameState(CGameState * game);
void freeCGameState(CGameState * game);
int isValidMove(CGameState * game, int board, int row, int column);
int isBoardWon (CGameState * game, int board, int row, int column);
int isGameWon(CGameState * game, int board);
int playTurn(CGameState * game, int board, int row, int column);
double countMoves(CGameState *game);
double countMovesLayers(CGameState *game, int layers);
Coord *chooseMoveFullBoard(CGameState *game);
Coord *chooseMoveSingleGrid(CGameState *game, unsigned char board);

Coord * getMoves(CGameState *game);
CGameState * copyCGameState(CGameState * copy, CGameState * original);

int evaluateBoard(CGameState * game);
int evaluateGrid(CGameState * game,int grid);
int staticHeuristic(CGameState * game);
int staticHeuristicWrapper(CGameState game);

int minimax(CGameState * game, int depth, int alpha, int beta, bool maximize);
int minimaxWrapper(CGameState game, int depth, int alpha, int beta, bool maximize);
#endif