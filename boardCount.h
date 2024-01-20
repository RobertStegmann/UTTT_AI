#ifndef _BOARDCOUNT_H
#define _BOARDCOUNT_H

#include <pthread.h>     /* pthreads library */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 
#include <time.h>
#include <string.h> 
#include <stdbool.h>
#include <sys/random.h>
#include <math.h>

#define BOARDSIZE 81
#define GRIDSIZE 9

#define MAX_THREADS 4

#define ANYBOARD 9

#define X_VAL 1
#define O_VAL 2

#define OPEN_VAL 0
#define STALEMATE 3
#define GAME_WON 1
#define NO_WIN 0
#define ROW_DIMENSION 3
#define COL_DIMENSION ROW_DIMENSION
#define VICTORY_VALUE 1000000

#define MAX_MOVES (BOARDSIZE+1)

#define BOARD_VALUE 28
#define GRID_VALUE 2
#define PLAYABLE_VALUE 1

#define STATESIZE 64


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
    int length;
    Coord moves[MAX_MOVES];
} MoveList;

typedef struct {
    int layers;
    Coord coords;
} Args;

typedef struct {
    int boardVal;
    int gridVal;
    int playableVal;
    int maxRuns;
    int index;
    int montePolicy;
    int threads;
} HeuristicVal;

typedef struct {
    CGameState game;
    int maxRuns;
    int montePolicy;
    int seed;
    int eval;
} MCHuerArg;

typedef struct {
    int rollout;
    int maxRuns;
    double c;
    int threads;
} MCST_Args;

typedef struct MonteCarloNode {
    CGameState game;
    struct MonteCarloNode * parent;
    MoveList possibleMoves;
    struct MonteCarloNode ** children;
    Coord move;
    int childNum;
    double N;
    double T;
} MonteCarloNode;

typedef struct RolloutArg {
    CGameState game;
    unsigned char player;
    int policy;
    int seed;
    int result;
} RolloutArg;

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
void revertTurn(CGameState *game, int board, int row, int column, unsigned char previousBoard);

void chooseMoveListSingleGrid(CGameState *game, MoveList * moves, unsigned char board);
void chooseMoveListFullBoard(CGameState *game, MoveList * moves);
void getMovesList(CGameState *game, MoveList * moves);

void shuffleMoveList(MoveList * list);
void shuffleMoves(Coord * moves, int moveCount) ;

Coord * trimMoves(Coord * moves, int * length);

CGameState * copyCGameState(CGameState * copy, CGameState * original);

int evaluateBoard(CGameState * game,HeuristicVal * val);
int evaluateGrid(CGameState * game,int grid,HeuristicVal * val);

int staticHeuristic(CGameState * game, HeuristicVal * val);
int staticHeuristicWrapper(CGameState game, HeuristicVal val);

int minimax(CGameState * game, int depth, int alpha, int beta, bool maximize, int heuristic (CGameState *,HeuristicVal * val), HeuristicVal * val);
int minimaxWrapper(CGameState game, int depth, int alpha, int beta, bool maximize, HeuristicVal val);

int evaluateAndRecordBoard(CGameState * game, int * boardRelevance, HeuristicVal * val);
int evaluateGridAndRecord(CGameState * game,int grid,bool * winnable, HeuristicVal * val);

int playableBoardHeuristic(CGameState * game, HeuristicVal * val);
int playableBoardHeuristicWrapper(CGameState game, HeuristicVal val);

int randomMove(CGameState * game);
int chooseRandomMove(CGameState * game, MoveList * moves);
int chooseWinningMove(CGameState * game, MoveList * moves);
int chooseWinLose(CGameState * game, MoveList * moves);

int simulateGame(CGameState * game, int policy);

int monteCarloHeuristic(CGameState * game, HeuristicVal * val);
int monteCarloHeuristicWrapper(CGameState game,HeuristicVal val);

Coord monteCarloTreeSearch(CGameState game, MCST_Args args);

double calcUCB(MonteCarloNode * node, double c);
void intializeRoot(MonteCarloNode * root, CGameState * game);
MonteCarloNode * createNode(CGameState * game, MonteCarloNode * parent, Coord * move);
void expand(MonteCarloNode * node);
MonteCarloNode * traverse(MonteCarloNode * node, double c);
double calcUCB(MonteCarloNode * node, double c);
double rollout(MonteCarloNode * node,unsigned char player, MCST_Args * args);
void backpropogate(MonteCarloNode * node, double result);
void freeMonteCarloTree(MonteCarloNode * root);
void freeMonteCarloNode(MonteCarloNode * node);

void * rollout_thread(void * r_arg);
int simulateGame_thread(CGameState * game, int policy,struct random_data * buf);
int chooseWinLose_thread(CGameState * game, MoveList * moves, struct random_data * buf);
int chooseWinningMove_thread(CGameState * game, MoveList * moves, struct random_data * buf);
int chooseRandomMove_thread(CGameState * game, MoveList * moves, struct random_data * buf);

void * monteCarloHeuristic_thread(void * args);

#endif