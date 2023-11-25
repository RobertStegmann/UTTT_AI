#include "boardCount.h"

int evaluateBoard(CGameState * game, HeuristicVal * val) {
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
            evaluation += val->boardVal*rcCount[i][0]*rcCount[i][0];
        } else if (rcCount[i][0] == 0 && rcCount[i][2] == 0){
            evaluation -= val->boardVal*rcCount[i][1]*rcCount[i][1];
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation += val->boardVal*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
        } else if (rcCount[i+ROW_DIMENSION][0] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation -= val->boardVal*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
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
        evaluation += val->boardVal*xCount*xCount;
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= val->boardVal*oCount*oCount;
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
        evaluation += val->boardVal*xCount*xCount;
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= val->boardVal*oCount*oCount;
    }     
            
    return evaluation;
}

int evaluateGrid(CGameState * game,int grid,HeuristicVal * val) {
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
            evaluation += val->gridVal*rcCount[i][0]*rcCount[i][0];
        } else if (rcCount[i][0] == 0){
            evaluation -= val->gridVal*rcCount[i][1]*rcCount[i][1];
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0){
            evaluation += val->gridVal*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
        } else if (rcCount[i+ROW_DIMENSION][0] == 0){
            evaluation -= val->gridVal*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
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
        evaluation += val->gridVal*xCount*xCount;
    } else if (xCount == 0){
        evaluation -= val->gridVal*oCount*oCount;
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
        evaluation += val->gridVal*xCount*xCount;
    } else if (xCount == 0){
        evaluation -= val->gridVal*oCount*oCount;
    }     
            
    return evaluation;
}

int staticHeuristic(CGameState * game, HeuristicVal * val) {
    int evaluation = evaluateBoard(game,val);
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
            gridEval = evaluateGrid(game,grid,val);
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

int staticHeuristicWrapper(CGameState game, HeuristicVal val) {
    return staticHeuristic(&game,&val);
}

int minimax(CGameState * game, int depth, int alpha, int beta, bool maximize, int heuristic (CGameState *,HeuristicVal *), HeuristicVal * val) {
    int bestEval;
    int eval;
    int a = alpha;
    int b = beta;
    CGameState * tempGame;
    Coord * possibleMoves;
    if (game->gameWon != NO_WIN) {
        if (game->gameWon == GAME_WON) {
            if (game->currentTurn == X_VAL) {
                return VICTORY_VALUE;
            } else {
                return -VICTORY_VALUE;
            }
        } else {
            return 0;
        }
    } else if (depth == 0) {
        return heuristic(game,val);
    }
    tempGame = createCGameState();
    possibleMoves = getMoves(game);
    if (maximize) {
        bestEval = -VICTORY_VALUE;
        for (int i = 0; possibleMoves[i].board != 10; i++)
        {
            copyCGameState(tempGame,game);
            playTurn(tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
            eval = minimax(tempGame,depth-1,a,b,false,heuristic,val);
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
            eval = minimax(tempGame,depth-1,a,b,true,heuristic,val);
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

int minimaxWrapper(CGameState game, int depth, int alpha, int beta, bool maximize, HeuristicVal val) {
    int (*heurisitics[])(CGameState *,HeuristicVal *) = {
        staticHeuristic,
        playableBoardHeuristic,
        monteCarloHeuristic
    };
    srandom(time(NULL));
    return minimax(&game, depth, alpha, beta, maximize,heurisitics[val.index],&val);
}

int evaluateAndRecordBoard(CGameState * game, int * boardRelevance, HeuristicVal * val) {
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
            evaluation += val->boardVal*rcCount[i][0]*rcCount[i][0];
            for (int j = 0; j < COL_DIMENSION; j++) {
                *((boardRelevance+i*ROW_DIMENSION)+j)+=rcCount[i][0]+1;
            }
        } else if (rcCount[i][0] == 0 && rcCount[i][2] == 0){
            evaluation -= val->boardVal*rcCount[i][1]*rcCount[i][1];
            for (int j = 0; j < COL_DIMENSION; j++) {
                *((boardRelevance+i*ROW_DIMENSION)+j)+=rcCount[i][1]+1;
            }
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation += val->boardVal*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
            for (int j = 0; j < ROW_DIMENSION; j++) {
                *((boardRelevance+j*ROW_DIMENSION)+i)+=rcCount[i+ROW_DIMENSION][0]+1;
            }
        } else if (rcCount[i+ROW_DIMENSION][0] == 0 && rcCount[i+ROW_DIMENSION][2] == 0){
            evaluation -= val->boardVal*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
            for (int j = 0; j < ROW_DIMENSION; j++) {
                *((boardRelevance+j*ROW_DIMENSION)+i)+=rcCount[i+ROW_DIMENSION][1]+1;
            }
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
        evaluation += val->boardVal*xCount*xCount;
        for (int i = 0; i < ROW_DIMENSION; i++) {
            *((boardRelevance+i*ROW_DIMENSION)+i)+=xCount+1;
        }
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= val->boardVal*oCount*oCount;
        for (int i = 0; i < ROW_DIMENSION; i++) {
            *((boardRelevance+i*ROW_DIMENSION)+i)+=oCount+1;
        }
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
        evaluation += val->boardVal*xCount*xCount;
        a = 2;
        for (int i = 0; i < ROW_DIMENSION; i++) {
            *((boardRelevance+a*ROW_DIMENSION)+i)+=xCount+1;
            a--;
        }
    } else if (xCount == 0 && stalemateCount == 0){
        evaluation -= val->boardVal*oCount*oCount;
        a = 2;
        for (int i = 0; i < ROW_DIMENSION; i++) {
            *((boardRelevance+a*ROW_DIMENSION)+i)+=oCount+1;
            a--;
        }
    }     
            
    return evaluation;
}

int evaluateGridAndRecord(CGameState * game,int grid,bool * winnable,HeuristicVal * val) {
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
            evaluation += val->gridVal*rcCount[i][0]*rcCount[i][0];
            *winnable = true;
        } else if (rcCount[i][0] == 0){
            evaluation -= val->gridVal*rcCount[i][1]*rcCount[i][1];
            *winnable = true;
        }
        if (rcCount[i+ROW_DIMENSION][1] == 0){
            evaluation += val->gridVal*rcCount[i+ROW_DIMENSION][0]*rcCount[i+ROW_DIMENSION][0];
            *winnable = true;
        } else if (rcCount[i+ROW_DIMENSION][0] == 0){
            evaluation -= val->gridVal*rcCount[i+ROW_DIMENSION][1]*rcCount[i+ROW_DIMENSION][1];
            *winnable = true;
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
        evaluation += val->gridVal*xCount*xCount;
        *winnable = true;
    } else if (xCount == 0){
        evaluation -= val->gridVal*oCount*oCount;
        *winnable = true;
    }

    xCount = 0;
    oCount = 0;
    int a = 2;
    for (int i = 0; i < ROW_DIMENSION; i++) {
        if (game->board[grid][a][i] == X_VAL) {
            xCount++;
            *winnable = true;
        } else if (game->board[grid][a][i] == O_VAL) {   
            oCount++;
            *winnable = true;
        }
        a--;
    }
    if (oCount == 0){
        evaluation += val->gridVal*xCount*xCount;
        *winnable = true;
    } else if (xCount == 0){
        evaluation -= val->gridVal*oCount*oCount;
        *winnable = true;
    }     
            
    return evaluation;
}

int playableBoardHeuristic(CGameState * game, HeuristicVal * val) {
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
    bool winnable;
    int relevantBoard[ROW_DIMENSION][COL_DIMENSION];
    memset(relevantBoard,0,sizeof(int)*ROW_DIMENSION*COL_DIMENSION);
    int evaluation = evaluateAndRecordBoard(game,&relevantBoard[0][0],val);
    for (int grid = 0; grid < 9; grid++) {
        r = (int)(grid / ROW_DIMENSION);
        c = grid % COL_DIMENSION;
        if (game->boardsWon[r][c] == 0) {
            winnable = false;
            gridEval = evaluateGridAndRecord(game,grid,&winnable,val);
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
            if ((game->currentBoard == 9 || grid == game->currentBoard) && winnable) {
                evaluation += game->currentTurn == X_VAL ? relevantBoard[r][c]*val->playableVal : -relevantBoard[r][c]*val->playableVal;
            }
        }
    }
    return evaluation;
}

int playableBoardHeuristicWrapper(CGameState game,HeuristicVal val) {
    return playableBoardHeuristic(&game, &val);
}

int monteCarloHeuristic(CGameState * game, HeuristicVal * val) {
    int evaluation = 0;
    CGameState * tempGame = createCGameState();
    for (int i = 0; i < val->maxRuns; i++) {
        copyCGameState(tempGame,game);
        if (simulateGame(tempGame) == GAME_WON) {
            evaluation += tempGame->currentTurn == X_VAL ? 1 : -1;
        }
    }
    freeCGameState(tempGame);
    return evaluation;
}

int monteCarloHeuristicWrapper(CGameState game,HeuristicVal val) {
    srandom(time(NULL));
    return monteCarloHeuristic(&game, &val);
}

typedef struct {
    CGameState * game;
    MonteCarloNode * parent;
    Coord * moves;
    MonteCarloNode ** children;
    int childNum;
    int visits;
    int wins;
} MonteCarloNode;

int monteCarloTreeSearch(CGameState game, MoveList moves, int maxRuns) {
    int bestMoveIndex = 0;

    for (int i = 0; i < maxRuns; i++) {


    }

    return bestMoveIndex;
}

MonteCarloNode * traverse(MonteCarloNode * node) {
    MonteCarloNode * currentChild = NULL;
    MonteCarloNode * bestChild = NULL;
    if (node->childNum > 0) {
        bestChild = node->children[0];
        currentChild = node->children[0];
        for (int i = 0; i < node->childNum; i++) {

        }
    } else {
        return node;
    }
}

