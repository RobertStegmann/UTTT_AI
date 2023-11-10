#include "boardCount.h"

int evaluateBoard(CGameState * game) {
    int evaluation = 0;
    int rcCount[6][3];

    memset(rcCount,0,sizeof(int)*18);
    // Rows and columns
    for (int i = 0; i < ROW_DIMENSION; i++) {
        for (int j = 0; j < COL_DIMENSION; j++) {
            if (game->boardsWon[i][j] == X_VAL) {
                rcCount[i][0]++;
            } else if (game->boardsWon[i][j] == O_VAL) {   
                rcCount[i][1]++;
            } else if (game->boardsWon[i][j] == STALEMATE) {
                rcCount[i][2]++;
            }
            if (game->boardsWon[j][i] == X_VAL) {
                rcCount[i+ROW_DIMENSION][0]++;
            } else if (game->boardsWon[j][i] == O_VAL) {   
                rcCount[i+ROW_DIMENSION][1]++;
            } else if (game->boardsWon[j][i] == STALEMATE) {
                rcCount[i+ROW_DIMENSION][2]++;
            }
        }  
        if (rcCount[i][1] == 0 && rcCount[i][2] == 0){
            evaluation += BOARD_VALUE*rcCount[i][0]*rcCount[i][0];
        } else if (rcCount[i][0] == 0 && rcCount[i][2] == 0){
            evaluation -= BOARD_VALUE*rcCount[i][1]*rcCount[i][1];
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation += BOARD_VALUE*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
        } else if (rcCount[i+ROW_DIMENSION][0] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation -= BOARD_VALUE*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
        }
    }

    int xCount = 0;
    int oCount = 0;
    int stalemateCount = 0;
    
    for (int i = 0; i < ROW_DIMENSION; i++) {
        if (game->boardsWon[i][i] == X_VAL) {
            xCount++;
        } else if (game->boardsWon[i][i] == O_VAL) {   
            oCount++;
        } else if (game->boardsWon[i][i] == STALEMATE) {
            stalemateCount++;
        }
    }
    if (oCount == 0 && stalemateCount == 0){
        evaluation += BOARD_VALUE*xCount*xCount;
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= BOARD_VALUE*oCount*oCount;
    }

    xCount = 0;
    oCount = 0;
    stalemateCount = 0;
    int a = 2;
     for (int i = 0; i < ROW_DIMENSION; i++) {
        if (game->boardsWon[a][i] == X_VAL) {
            xCount++;
        } else if (game->boardsWon[a][i] == O_VAL) {   
            oCount++;
        } else if (game->boardsWon[a][i] == STALEMATE) {
            stalemateCount++;
        }
        a--;
    }
    if (oCount == 0 && stalemateCount == 0){
        evaluation += BOARD_VALUE*xCount*xCount;
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= BOARD_VALUE*oCount*oCount;
    }     
            
    return evaluation;
}

int evaluateGrid(CGameState * game,int grid) {
    int evaluation = 0;
    int rcCount[6][2];
    memset(rcCount,0,sizeof(int)*12);
    // Rows and columns
    for (int i = 0; i < ROW_DIMENSION; i++) {
        for (int j = 0; j < COL_DIMENSION; j++) {
            if (game->board[grid][i][j] == X_VAL) {
                rcCount[i][0]++;
            } else if (game->board[grid][i][j] == O_VAL) {   
                rcCount[i][1]++;
            }
            if (game->board[grid][j][i] == X_VAL) {
                rcCount[i+ROW_DIMENSION][0]++;
            } else if (game->board[grid][j][i] == O_VAL) {   
                rcCount[i+ROW_DIMENSION][1]++;
            }
        }     
        if (rcCount[i][1] == 0){
            evaluation += GRID_VALUE*rcCount[i][0]*rcCount[i][0];
        } else if (rcCount[i][0] == 0){
            evaluation -= GRID_VALUE*rcCount[i][1]*rcCount[i][1];
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0){
            evaluation += GRID_VALUE*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
        } else if (rcCount[i+ROW_DIMENSION][0] == 0){
            evaluation -= GRID_VALUE*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
        }
    }

    int xCount = 0;
    int oCount = 0;
    
    for (int i = 0; i < ROW_DIMENSION; i++) {
        if (game->board[grid][i][i] == X_VAL) {
            xCount++;
        } else if (game->board[grid][i][i] == O_VAL) {   
            oCount++;
        }
    }
    if (oCount == 0){
        evaluation += GRID_VALUE*xCount*xCount;
    } else if (xCount == 0){
        evaluation -= GRID_VALUE*oCount*oCount;
    }

    xCount = 0;
    oCount = 0;
    int a = 2;
    for (int i = 0; i < ROW_DIMENSION; i++) {
        if (game->board[grid][a][i] == X_VAL) {
            xCount++;
        } else if (game->board[grid][a][i] == O_VAL) {   
            oCount++;
        }
        a--;
    }
    if (oCount == 0){
        evaluation += GRID_VALUE*xCount*xCount;
    } else if (xCount == 0){
        evaluation -= GRID_VALUE*oCount*oCount;
    }     
            
    return evaluation;
}

int staticHeuristic(CGameState * game) {
    int evaluation = evaluateBoard(game);
    int gridEval = 0;
    int r = 0;
    int c = 0;
    int a = 2;
    int otherCoords[3][2] = {{1,2},{0,2},{0,1}};
    int upperRightDiagonal[3][2][2] = {{{1,1},{2,0}},
                                        {{0,2},{2,0}},
                                        {{0,2},{1,1}}};
    int rcCount[2][3];
    int xCount = 0;
    int oCount = 0;
    int stalemateCount = 0;
    for (int grid = 0; grid < 9; grid++) {
        r = (int)(grid / ROW_DIMENSION);
        c = grid % COL_DIMENSION;
        if (game->boardsWon[r][c] == 0) {
            gridEval = evaluateGrid(game,grid);
            memset(rcCount,0,sizeof(int)*6);

            for (int i = 0; i < 2; i++) {
                if (game->boardsWon[r][otherCoords[c][i]] == X_VAL) {
                    rcCount[0][0]++;
                } else if (game->boardsWon[r][otherCoords[c][i]] == O_VAL) {   
                    rcCount[0][1]++;
                } else if (game->boardsWon[r][otherCoords[c][i]] == STALEMATE) {
                    rcCount[0][2]++;
                }
                if (game->boardsWon[otherCoords[r][i]][c] == X_VAL) {
                    rcCount[1][0]++;
                } else if (game->boardsWon[otherCoords[r][i]][c] == O_VAL) {   
                    rcCount[1][1]++;
                } else if (game->boardsWon[otherCoords[r][i]][c] == STALEMATE) {
                    rcCount[1][2]++;
                } 
            }
            if (rcCount[0][2] == 0 && (rcCount[0][0] == 0 || rcCount[0][1] == 0)) {
                evaluation += gridEval;
            }
            if (rcCount[1][2] == 0 && (rcCount[1][0] == 0 || rcCount[1][1] == 0)) {
                evaluation += gridEval;
            }

            if (r == c) {
                xCount = 0;
                oCount = 0;
                stalemateCount = 0;

                for (int i = 0; i < 2; i++) {  
                    if (game->boardsWon[otherCoords[r][i]][otherCoords[r][i]] == X_VAL) {
                        xCount++;
                    } else if (game->boardsWon[otherCoords[r][i]][otherCoords[r][i]]  == O_VAL) {   
                        oCount++;
                    } else if (game->boardsWon[otherCoords[r][i]][otherCoords[r][i]]  == STALEMATE) {
                        stalemateCount++;
                    }
                }

                if (stalemateCount == 0 && (xCount == 0 || oCount == 0)) {
                    evaluation += gridEval;
                }
            }

            if ((r+c) == 2) {
                xCount = 0;
                oCount = 0;
                stalemateCount = 0;
                for (int i = 0; i < 2; i++) {
                    if (game->boardsWon[upperRightDiagonal[r][i][0]][upperRightDiagonal[r][i][1]] == X_VAL) {
                        xCount++;
                    } else if (game->boardsWon[upperRightDiagonal[r][i][0]][upperRightDiagonal[r][i][1]]  == O_VAL) {   
                        oCount++;
                    } else if (game->boardsWon[upperRightDiagonal[r][i][0]][upperRightDiagonal[r][i][1]]  == STALEMATE) {
                        stalemateCount++;
                    }
                }

                if (stalemateCount == 0 && (xCount == 0 || oCount == 0)) {
                    evaluation += gridEval;
                }
            }
        }
    }
    return evaluation;
}

int staticHeuristicWrapper(CGameState game) {
    return staticHeuristic(&game);
}

int minimax(CGameState * game, int depth, int alpha, int beta, bool maximize) {
    int bestEval;
    int eval;
    int a = alpha;
    int b = beta;
    CGameState * tempGame;
    Coord * possibleMoves;
    if (game->gameWon != NO_WIN) {
        if (game->gameWon == X_VAL) {
            return VICTORY_VALUE;
        } else if (game->gameWon == O_VAL) {
            return -VICTORY_VALUE;
        } else {
            return 0;
        }
    } else if (depth == 0) {
        return staticHeuristic(game);
    }
    tempGame = createCGameState();
    possibleMoves = getMoves(game);
    if (maximize) {
        bestEval = -VICTORY_VALUE;
        for (int i = 0; possibleMoves[i].board != 10; i++)
        {
            copyCGameState(tempGame,game);
            playTurn(tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
            eval = minimax(tempGame,depth-1,a,b,false);
            bestEval = MAX(bestEval,eval);
            a = MAX(a,eval);
            if (b <= a) {
                break;
            }
        }
    } else {
        bestEval = VICTORY_VALUE;
        for (int i = 0; possibleMoves[i].board != 10; i++)
        {
            copyCGameState(tempGame,game);
            playTurn(tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
            eval = minimax(tempGame,depth-1,a,b,true);
            bestEval = MIN(bestEval,eval);
            b = MIN(b,eval);
            if (b <= a) {
                break;
            }
        }
    }
    free(possibleMoves);
    freeCGameState(tempGame);
    return bestEval;
}

int minimaxWrapper(CGameState game, int depth, int alpha, int beta, bool maximize) {
    return minimax(&game, depth, alpha, beta, maximize);
}