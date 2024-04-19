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
    errorCode = pthread_create(&topcentre_id, NULL, &countTopCentre, NULL);
    if (errorCode) {
        fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
    }
    errorCode = pthread_create(&centre_id, NULL, &countCentre, NULL);
    if (errorCode) {
        fprintf(stderr,"ERROR: errorCode = pthread_create() failed\n");
    }
    pthread_join(topleft_id, NULL);
    pthread_join(topcentre_id, NULL);
    pthread_join(centre_id, NULL);
    time_t end = time(NULL);
    printf("Execution time in seconds: %ld\n",(end-begin));
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
    for (int i = 0; i < 6; i++)
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
    arg[2].row = 1;
    arg[2].column = 1;
    int errorCode;
    for (int i = 0; i < 3; i++)
    {
        arg[i].board = 4;
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
    CGameState *game = createCGameState();
    double moveCount = 1;
    playTurn(game, board, row, column);
    moveCount += countMoves(game);
    printf("Possible boards from starting at %d,%d,%d: %.0f\n", board, row, column, moveCount);
}

double countMoves(CGameState *game)
{
    double moveCount = 0;
    Coord *possibleMoves;
    possibleMoves = getMoves(game);
    CGameState *tempGame = createCGameState();
    for (int i = 0; possibleMoves[i].board != 10; i++)
    {
        copyCGameState(tempGame,game);
        playTurn(tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
        moveCount++;
        if (tempGame->gameWon == 0)
        {
            moveCount += countMoves(tempGame);
        }
        
    }
    freeCGameState(tempGame);
    free(possibleMoves);
}