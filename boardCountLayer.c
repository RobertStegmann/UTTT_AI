#include "boardCount.h"

//Ran at 10:28 2023-09-19

int main(int argc, char * argv[])
{
    if (argc == 2) {
        pthread_t topleft_id;
        pthread_t topcentre_id;
        pthread_t centre_id;
        int errorCode;
        int maxLayers = atoi(argv[1]);
        time_t begin = time(NULL);
        errorCode = pthread_create(&topleft_id, NULL, &countTopLeftLayers, (void *) &maxLayers);
        if (errorCode)
        {
            fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
        }
        errorCode = pthread_create(&topcentre_id, NULL, &countTopCentreLayers, (void *) &maxLayers);
        if (errorCode) {
            fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
        }
        errorCode = pthread_create(&centre_id, NULL, &countCentreLayers, (void *) &maxLayers);
        if (errorCode) {
            fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
        }
        pthread_join(topleft_id, NULL);
        pthread_join(topcentre_id, NULL);
        pthread_join(centre_id, NULL);
        time_t end = time(NULL);
        printf("Execution time in seconds: %d\n",(end-begin));
    } else {
        printf("Usage: ./boardCountLayer [number of layers]\n");
    }
}

void *countTopLeftLayers(void * mLayers)
{
    pthread_t t_id[6];
    int threadCount = 0;
    int maxLayers = *((int *)mLayers);
    Args arg[6];
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            arg[threadCount].coords.board = 0;
            arg[threadCount].coords.row = i;
            arg[threadCount].coords.column = j;
            arg[threadCount].layers = maxLayers;
            errorCode = pthread_create((&t_id[threadCount]), NULL, &countFromStartWrapperLayers, (void *)(&arg[threadCount]));
            if (errorCode)
            {
                fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
            }
            threadCount++;
        }
    }
    for (int i = 0; i < 6; i++)
    {
        pthread_join(t_id[i], NULL);
    }
    pthread_exit(NULL);
}

void *countTopCentreLayers(void * mLayers)
{
    pthread_t t_id[6];
    int threadCount = 0;
    int maxLayers = *((int *)mLayers);
    Args arg[6];
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            arg[threadCount].coords.board = 1;
            arg[threadCount].coords.row = i;
            arg[threadCount].coords.column = j;
            arg[threadCount].layers = maxLayers;
            errorCode = pthread_create((&t_id[threadCount]), NULL, &countFromStartWrapperLayers, (void *)(&arg[threadCount]));;
            if (errorCode)
            {
                fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
            }
            threadCount++;
        }
    }

    for (int i = 0; i < 6; i++)
    {
        pthread_join(t_id[i], NULL);
    }
    pthread_exit(NULL);
}

void *countCentreLayers(void * mLayers)
{
    pthread_t t_id[3];
    int maxLayers = *((int *)mLayers);
    Args arg[3];
    arg[0].coords.row = 0;
    arg[0].coords.column = 0;
    arg[1].coords.row = 0;
    arg[1].coords.column = 1;
    arg[2].coords.row = 1;
    arg[2].coords.column = 1;
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        arg[i].coords.board = 4;
        arg[i].layers = maxLayers;
        errorCode = pthread_create((&t_id[i]), NULL, &countFromStartWrapperLayers, (void *)(&arg[i]));
        if (errorCode)
        {
            fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
        }
    }

    for (int i = 0; i < 3; i++)
    {
        pthread_join(t_id[i], NULL);
    }
    pthread_exit(NULL);
}

void *countFromStartWrapperLayers(void *arg)
{
    Args * arguments = (Args*)arg;
    countFromStartLayers(arguments->coords.board, arguments->coords.row, arguments->coords.column,arguments->layers);
    pthread_exit(NULL);
}

void countFromStartLayers(int board, int row, int column, int layers)
{
    GameState *game = createGameState();
    double moveCount = 1;
    playTurn(game, board, row, column);
    moveCount += countMovesLayers(game, layers-1);
    printf("Possible boards from starting at %d,%d,%d after %d moves: %.0f\n", board, row, column, layers, moveCount);
}

/* Create a GameState struct */
GameState *createGameState()
{
    GameState *newGame = calloc(1, sizeof(GameState));
    newGame->board = calloc(GRIDSIZE, sizeof(char **));
    for (int i = 0; i < GRIDSIZE; i++)
    {
        newGame->board[i] = calloc(ROW_DIMENSION, sizeof(char *));
        for (int j = 0; j < ROW_DIMENSION; j++)
        {
            newGame->board[i][j] = calloc(COL_DIMENSION, sizeof(char));
        }
    }
    newGame->boardsWon = calloc(ROW_DIMENSION, sizeof(char *));
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        newGame->boardsWon[i] = calloc(COL_DIMENSION, sizeof(char));
    }

    newGame->currentBoard = ANYBOARD;
    newGame->currentTurn = X_VAL;
    newGame->gameWon = NO_WIN;

    return newGame;
}

/* Clone a GameState struct*/
GameState *cloneGameState(GameState *game)
{
    GameState *newGame = createGameState();

    for (int i = 0; i < GRIDSIZE; i++)
    {
        for (int j = 0; j < ROW_DIMENSION; j++)
        {
            for (int k = 0; k < COL_DIMENSION; k++)
            {
                newGame->board[i][j][k] = game->board[i][j][k];
            }
        }
    }

    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            newGame->boardsWon[i][j] = game->boardsWon[i][j];
        }
    }

    newGame->currentBoard = game->currentBoard;
    newGame->currentTurn = game->currentTurn;
    newGame->gameWon = game->gameWon;

    return newGame;
}

/* Free a GameState struct */
void freeGameState(GameState *game)
{
    for (int i = 0; i < GRIDSIZE; i++)
    {
        for (int j = 0; j < ROW_DIMENSION; j++)
        {
            free(game->board[i][j]);
            game->board[i][j] = NULL;
        }
        free(game->board[i]);
        game->board[i] = NULL;
    }
    free(game->board);
    game->board = NULL;

    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        free(game->boardsWon[i]);
        game->boardsWon[i] = NULL;
    }

    free(game->boardsWon);
    game->boardsWon = NULL;
    free(game);
    game = NULL;
}

int isValidMove(GameState *game, int board, int row, int column)
{
    if (board == game->currentBoard || game->currentBoard == 9)
    {
        if (game->board[board][row][column] != 0)
        {
            return 0;
        }
        int r = (int)(board / ROW_DIMENSION);
        int c = board % COL_DIMENSION;
        if (game->boardsWon[r][c] != 0)
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

int isBoardWon(GameState *game, int board, int row, int column)
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

int isGameWon(GameState *game, int board)
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

int playTurn(GameState *game, int board, int row, int column)
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

double countMovesLayers(GameState *game, int layers)
{
    //printf("countMoves()\n");
    double moveCount = 0;
    Coord *possibleMoves;
    if (game->currentBoard == 9)
    {
        possibleMoves = chooseMoveFullBoard(game);
    }
    else
    {
        possibleMoves = chooseMoveSingleGrid(game, game->currentBoard);
    }
    GameState *tempGame;
    for (int i = 0; possibleMoves[i].board != 10; i++)
    {
        tempGame = cloneGameState(game);
        playTurn(tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
        moveCount++;
        if (tempGame->gameWon == 0 &&  0 < layers)
        {
            moveCount += countMovesLayers(tempGame, layers - 1);
        }
        freeGameState(tempGame);
    }
    free(possibleMoves);
}

Coord *chooseMoveFullBoard(GameState *game)
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

Coord *chooseMoveSingleGrid(GameState *game, unsigned char board)
{
    Coord *possibleMoves = calloc(GRIDSIZE, sizeof(Coord));
    int arraySize = 0;
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            if (game->board[board][i][j] == 0)
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
