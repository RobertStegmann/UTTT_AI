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
    CGameState *game = createCGameState();
    double moveCount = 1;
    playTurn(game, board, row, column);
    moveCount += countMovesLayers(game, layers-1);
    printf("Possible boards from starting at %d,%d,%d after %d moves: %.0f\n", board, row, column, (layers+1), moveCount);
}

double countMovesLayers(CGameState *game, int layers)
{
    double moveCount = 0;
    Coord *possibleMoves;
    possibleMoves = getMoves(game);
    CGameState tempGame;
    for (int i = 0; possibleMoves[i].board != 10; i++)
    {
        copyCGameState(&tempGame,game);
        playTurn(&tempGame, possibleMoves[i].board, possibleMoves[i].row, possibleMoves[i].column);
        moveCount++;
        if (tempGame.gameWon == 0 &&  0 < layers)
        {
            moveCount += countMovesLayers(&tempGame, layers - 1);
        }
    }
    free(possibleMoves);
}
