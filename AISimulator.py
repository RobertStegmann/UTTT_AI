import GameState as g
import TicTacToeAI as AI
from prettytable import PrettyTable
from time import process_time
import Heuristics as h 

def simulateGames(AI_1:AI.TicTacToeAI, AI_2:AI.TicTacToeAI, gameNum=int):
    rounds = gameNum // 2
    wins = [[0,0],[0,0]]
    runTime = [[0.0,0.0],[0.0,0.0]]
    game = g.GameState()
    t_start = 0.0
    t_end = 0.0
    stalemates = 0
    Player1 = AI_1
    Player2 = AI_2
    for r in range(0,2):
        for i in range(0,rounds):
            game = g.GameState()
            while (game.gameWon == g.NO_WIN):
                if (game.currentTurn == 1):
                    t_start = process_time()  
                    moveAI = Player1.chooseMove(game)
                    t_end = process_time()
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])  
                    runTime[r][0] = runTime[r][0] + t_end - t_start 
                else:
                    t_start = process_time()  
                    moveAI = Player2.chooseMove(game)
                    t_end = process_time()
                    game.playTurn(moveAI[0],moveAI[1],moveAI[2])  
                    runTime[r][1] = runTime[r][1] + t_end - t_start 
            if (game.gameWon == g.GAME_WON):
                wins[r][game.currentTurn - 1] += 1
            else:
                stalemates = stalemates + 1
        Player1 = AI_2
        Player2 = AI_1
    
    winPerc_AI1 = 100*(wins[0][0]+wins[1][1]) / (2*rounds)
    winPerc_AI2 = 100*(wins[0][1]+wins[1][0]) / (2*rounds)
    
    table = PrettyTable(["AI","Round 1 Wins","Round 2 Wins","Total Wins","Stalemates","Total Rounds","Win %","Run Time"])
    table.add_row([AI_1.toString(),wins[0][0],wins[1][1],wins[0][0]+wins[1][1],stalemates,2*rounds,winPerc_AI1,runTime[0][0]+runTime[1][1]])
    table.add_row([AI_2.toString(),wins[0][1],wins[1][0],wins[0][1]+wins[1][0],stalemates,2*rounds,winPerc_AI2,runTime[0][1]+runTime[1][0]])
    print(table)
        
        

# allAIs = []
# allAIs.append(AI.RandomAI())
# for i in range(0,64):
#     allAIs.append(AI.ChooseWinLose(i))
# for i in range(0,len(allAIs)):
#     for j in range(i+1,len(allAIs)):
#        simulateGames(allAIs[i],allAIs[j],1000)
randomAI = AI.RandomAI()
mimimaxAIFour = AI.ChooseMinimax(4,h.StaticHeuristic())
mimimaxAIThree = AI.ChooseMinimax(3,h.StaticHeuristic())
mimimaxAITwo = AI.ChooseMinimax(2,h.StaticHeuristic())
mimimaxAITwoC = AI.ChooseMinimax(2,h.StaticHeuristicC())
minimaxCTwo = AI.ChooseMinimaxC(2)
minimaxCFour = AI.ChooseMinimaxC(4)
#mimimaxAIOne= AI.ChooseMinimax(1,h.StaticHeuristic())
chooseAI = AI.ChooseWinLose(0)
# simulateGames(randomAI,mimimaxAIThree,100)
#simulateGames(mimimaxAIThree,chooseAI,1000)
#simulateGames(minimaxCTwo,mimimaxAITwoC,100)
#simulateGames(mimimaxAITwo,mimimaxAITwoC,100)
#simulateGames(mimimaxAITwo,minimaxCTwo,100)
#simulateGames(mimimaxAITwo,chooseAI,100)
simulateGames(randomAI,minimaxCTwo,100)
simulateGames(randomAI,minimaxCFour,100)


