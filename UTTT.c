#include "boardCount.h"

/* Create a CGameState struct */
CGameState *createCGameState()
{
    CGameState *newGame = calloc(1, sizeof(CGameState));

    if (newGame == NULL) {
        fprintf(stderr,"Error: Calloc failed\n");
        exit(1);
    }

    newGame->currentBoard = ANYBOARD;
    newGame->currentTurn = X_VAL;
    newGame->gameWon = NO_WIN;

    return newGame;
}

/* Copy a CGameState struct*/
CGameState * copyCGameState(CGameState * copy, CGameState * original)
{
    if (copy == NULL) {
        fprintf(stderr,"Error: Null Copy\n");
        exit(1);
    } else if (original == NULL) {
        fprintf(stderr,"Error: Null Original\n");
        exit(1);
    }

    for (int i = 0; i < GRIDSIZE; i++)
    {
        for (int j = 0; j < ROW_DIMENSION; j++)
        {
            for (int k = 0; k < COL_DIMENSION; k++)
            {
                copy->board[i][j][k] = original->board[i][j][k];
            }
        }
    }

    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            copy->boardsWon[i][j] = original->boardsWon[i][j];
        }
    }

    copy->currentBoard = original->currentBoard;
    copy->currentTurn = original->currentTurn;
    copy->gameWon = original->gameWon;

    return copy;
}


/* Clone a CGameState struct*/
CGameState *cloneCGameState(CGameState *game)
{
    CGameState *newGame = calloc(1, sizeof(CGameState));
    return copyCGameState(newGame,game);
}

/* Free a CGameState struct */
void freeCGameState(CGameState *game)
{
    free(game);
    game = NULL;
}

int isValidMove(CGameState *game, int board, int row, int column)
{
    if (board == game->currentBoard || game->currentBoard == ANYBOARD)
    {
        if (game->board[board][row][column] != OPEN_VAL)
        {
            return 0;
        }
        int r = (int)(board / ROW_DIMENSION);
        int c = board % COL_DIMENSION;
        if (game->boardsWon[r][c] != OPEN_VAL)
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
}

int isBoardWon(CGameState *game, int board, int row, int column)
{
    if (game->board[board][row][0] == game->board[board][row][1] && game->board[board][row][1] == game->board[board][row][2])
    {
        return GAME_WON;
    }
    else if (game->board[board][0][column] == game->board[board][1][column] && game->board[board][1][column] == game->board[board][2][column])
    {
        return GAME_WON;
    }
    else if (row == column && game->board[board][0][0] == game->board[board][1][1] && game->board[board][1][1] == game->board[board][2][2])
    {
        return GAME_WON;
    }
    else if ((row + column) == 2 && game->board[board][0][2] == game->board[board][1][1] && game->board[board][1][1] == game->board[board][2][0])
    {
        return GAME_WON;
    }
    else
    {
        for (int i = 0; i < ROW_DIMENSION; i++)
        {
            for (int j = 0; j < COL_DIMENSION; j++)
            {
                if (game->board[board][i][j] == 0)
                {
                    return NO_WIN;
                }
            }
        }
        return STALEMATE;
    }
}

int isGameWon(CGameState *game, int board)
{
    int row = (int)(board / ROW_DIMENSION);
    int column = board % COL_DIMENSION;
    if (game->boardsWon[row][0] == game->boardsWon[row][1] && game->boardsWon[row][1] == game->boardsWon[row][2])
    {
        return GAME_WON;
    }
    else if (game->boardsWon[0][column] == game->boardsWon[1][column] && game->boardsWon[1][column] == game->boardsWon[2][column])
    {
        return GAME_WON;
    }
    else if (row == column && game->boardsWon[0][0] == game->boardsWon[1][1] && game->boardsWon[1][1] == game->boardsWon[2][2])
    {
        return GAME_WON;
    }
    else if ((row + column) == 2 && game->boardsWon[0][2] == game->boardsWon[1][1] && game->boardsWon[1][1] == game->boardsWon[2][0])
    {
        return GAME_WON;
    }
    else
    {
        for (int i = 0; i < ROW_DIMENSION; i++)
        {
            for (int j = 0; j < COL_DIMENSION; j++)
            {
                if (game->boardsWon[i][j] == 0)
                {
                    return NO_WIN;
                }
            }
        }
        return STALEMATE;
    }
}

int playTurn(CGameState *game, int board, int row, int column)
{
    // Move must be valid, so we don't need to check here
    game->board[board][row][column] = game->currentTurn;
    int boardWin = isBoardWon(game, board, row, column);
    int boardRow;
    int boardColumn;
    if (boardWin != NO_WIN)
    {
        int boardRow = (int)(board / ROW_DIMENSION);
        int boardColumn = board % COL_DIMENSION;
        game->boardsWon[boardRow][boardColumn] = boardWin == GAME_WON ? (unsigned char)game->currentTurn : STALEMATE;
        game->gameWon = (char)isGameWon(game, board);
        if (game->gameWon != NO_WIN)
        {
            return game->gameWon;
        }
    }

    game->currentTurn = game->currentTurn == X_VAL ? O_VAL : X_VAL;
    game->currentBoard = game->boardsWon[row][column] == NO_WIN ? (unsigned char)(COL_DIMENSION * row + column) : ANYBOARD;
    return NO_WIN;
}

Coord *chooseMoveFullBoard(CGameState *game)
{
    Coord *possibleMoves = calloc(BOARDSIZE, sizeof(Coord));
    int currentBoard = 0;
    int arraySize = 0;
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            if (game->boardsWon[i][j] == NO_WIN)
            {
                currentBoard = COL_DIMENSION * i + j;
                for (int k = 0; k < ROW_DIMENSION; k++)
                {
                    for (int l = 0; l < COL_DIMENSION; l++)
                    {
                        if (game->board[currentBoard][k][l] == 0)
                        {
                            possibleMoves[arraySize].board = currentBoard;
                            possibleMoves[arraySize].row = k;
                            possibleMoves[arraySize].column = l;
                            arraySize++;
                        }
                    }
                }
            }
        }
    }
    possibleMoves[arraySize].board = 10;
    return possibleMoves;
}

Coord *chooseMoveSingleGrid(CGameState *game, unsigned char board)
{
    Coord *possibleMoves = calloc(GRIDSIZE, sizeof(Coord));
    int arraySize = 0;
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            if (game->board[board][i][j] == OPEN_VAL)
            {
                possibleMoves[arraySize].board = board;
                possibleMoves[arraySize].row = i;
                possibleMoves[arraySize].column = j;
                arraySize++;
            }
        }
    }
    possibleMoves[arraySize].board = 10;
    return possibleMoves;
}

Coord * getMoves(CGameState *game) {
    Coord *possibleMoves;
    if (game->currentBoard == ANYBOARD)
    {
        possibleMoves = chooseMoveFullBoard(game);
    }
    else
    {
        possibleMoves = chooseMoveSingleGrid(game, game->currentBoard);
    }
    return possibleMoves;
}
