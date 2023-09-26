#include "boardCount.h"

int main()
{
    pthread_t topleft_id;
    pthread_t topcentre_id;
    pthread_t centre_id;
    int errorCode;
    time_t begin = time(NULL);
    errorCode = errorCode = pthread_create(&topleft_id, NULL, &countTopLeft, NULL);
    if (errorCode)
    {
        fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
    }
    errorCode = pthread_create(&topcentre_id, NULL, &countTopLeft, NULL);
    if (errorCode) {
        fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
    }
    errorCode = pthread_create(&centre_id, NULL, &countTopLeft, NULL);
    if (errorCode) {
        fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
    }
    pthread_join(topleft_id, NULL);
    pthread_join(topcentre_id, NULL);
    pthread_join(centre_id, NULL);
    time_t end = time(NULL);
    printf("Execution time in seconds: %d\n",(end-begin));
}

void *countTopLeft(void *foo)
{
    pthread_t t_id[6];
    int threadCount = 0;
    Coord arg[6];
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            arg[threadCount].board = 0;
            arg[threadCount].row = i;
            arg[threadCount].column = j;
            errorCode = pthread_create((&t_id[threadCount]), NULL, &countFromStartWrapper, (void *)(&arg[threadCount]));
            if (errorCode)
            {
                fprintf(stderr, "ERROR: errorCode = pthread_create() failed\n");
            }
            threadCount++;
        }
    }
    for (int i = 0; i < 1; i++)
    {
        pthread_join(t_id[i], NULL);
    }
    pthread_exit(NULL);
}

void *countTopCentre(void *foo)
{
    pthread_t t_id[6];
    int threadCount = 0;
    Coord arg[6];
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            arg[threadCount].board = 1;
            arg[threadCount].row = i;
            arg[threadCount].column = j;
            errorCode = pthread_create((&t_id[threadCount]), NULL, &countFromStartWrapper, (void *)(&arg[threadCount]));;
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

void *countCentre(void *foo)
{
    pthread_t t_id[3];
    Coord arg[3];
    arg[0].row = 0;
    arg[0].column = 0;
    arg[1].row = 0;
    arg[1].column = 1;
    arg[1].row = 1;
    arg[1].column = 1;
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        arg[i].board = 5;
        errorCode = pthread_create((&t_id[i]), NULL, &countFromStartWrapper, (void *)(&arg[i]));
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

void *countFromStartWrapper(void *arg)
{
    Coord *coords = (Coord *)arg;
    countFromStart(coords->board, coords->row, coords->column);
    pthread_exit(NULL);
}

void countFromStart(int board, int row, int column)
{
    GameState *game = createGameState();
    double moveCount = 1;
    playTurn(game, board, row, column);
    moveCount += countMoves(game);
    printf("Possible moves from starting at %d,%d,%d: %.0f \n", board, row, column, moveCount);
}

/* Create a GameState struct */
GameState *createGameState()
{
    GameState *newGame = calloc(1, sizeof(GameState));
    if (newGame == NULL)
    {
        fprintf(stderr, "newGame in createGameState() failed to allocate\n");
        return NULL;
    }
    newGame->board = calloc(GRIDSIZE, sizeof(char **));
    if (newGame->board == NULL)
    {
        fprintf(stderr, "newGame->board in createGameState() failed to allocate\n");
        return NULL;
    }
    for (int i = 0; i < GRIDSIZE; i++)
    {
        newGame->board[i] = calloc(ROW_DIMENSION, sizeof(char *));
        if (newGame->board[i] == NULL)
        {
            fprintf(stderr, "newGame->board[%d] in createGameState() failed to allocate\n", i);
            return NULL;
        }
        for (int j = 0; j < ROW_DIMENSION; j++)
        {
            newGame->board[i][j] = calloc(COL_DIMENSION, sizeof(char));
            if (newGame->board[i][j] == NULL)
            {
                fprintf(stderr, "newGame->board[%d][%d] in createGameState() failed to allocate\n", i, j);
                return NULL;
            }
        }
    }
    newGame->boardsWon = calloc(ROW_DIMENSION, sizeof(char *));
    if (newGame->boardsWon == NULL)
    {
        fprintf(stderr, "newGame->boardsWon in createGameState() failed to allocate\n");
        return NULL;
    }
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        newGame->boardsWon[i] = calloc(COL_DIMENSION, sizeof(char));
        if (newGame->boardsWon[i] == NULL)
        {
            fprintf(stderr, "newGame->boardsWon[%d] in createGameState() failed to allocate\n", i);
            return NULL;
        }
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

double countMoves(GameState *game)
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
        if (tempGame->gameWon == 0)
        {
            moveCount += countMoves(tempGame);
        }
        freeGameState(tempGame);
    }
    free(possibleMoves);
}

Coord *chooseMoveFullBoard(GameState *game)
{
    //printf("chooseMoveFullBoard()\n");
    Coord *possibleMoves = calloc(BOARDSIZE, sizeof(Coord));
    if (possibleMoves == NULL)
    {
        fprintf(stderr, "possibleMoves in chooseMoveFullBoard() failed to allocate\n");
        return NULL;
    }
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
    //printf("chooseMoveSingleGrid()\n");
    Coord *possibleMoves = calloc(GRIDSIZE, sizeof(Coord));
    if (possibleMoves == NULL)
    {
        fprintf(stderr, "possibleMoves in chooseMoveSingleGrid() failed to allocate\n");
        return NULL;
    }
    int arraySize = 0;
    for (int i = 0; i < ROW_DIMENSION; i++)
    {
        for (int j = 0; j < COL_DIMENSION; j++)
        {
            //printf("Foo\n");
            //printf("game->board[%d][%d][%d]: %d\n",board,i,j,game->board[board][i][j]);
            if (game->board[board][i][j] == 0)
            {
                //printf("bar\n");
                possibleMoves[arraySize].board = board;
                possibleMoves[arraySize].row = i;
                possibleMoves[arraySize].column = j;
                arraySize++;
            }
           //printf("baz\n");
        }
    }
    possibleMoves[arraySize].board = 10;
    return possibleMoves;
}
