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
    print(table, flush=True)
        





            

# for i in range(0,len(minimaxPlayable)):
#     for j in range(i+1,len(minimaxPlayable)):
#          simulateGames(minimaxPlayable[i],minimaxPlayable[j],1000)

# for ms in minimaxStatic:
#     for ps in minimaxPlayable:
#         simulateGames(ms,ps,1000)

# randAI = AI.RandomAI()
# chooseWin = AI.ChooseWinLose(0)

# statHeur = AI.ChooseMinimax(2,h.StaticHeuristic())
# randHeur25 = AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=25))
# randHeur10 = AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=10))

# simulateGames(statHeur,randHeur25,500)


# minimaxStatic = [
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=10,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=11,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=12,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=13,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=14,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=15,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=20,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=25,gridVal=1)),
#     AI.ChooseMinimax(4,h.StaticHeuristic(boardVal=30,gridVal=1)),
# ]

# for i in range(0,len(minimaxStatic)):
#     for j in range(i+1,len(minimaxStatic)):
#             simulateGames(minimaxStatic[i],minimaxStatic[j],1000)
        

minimaxPlayable = [
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=130,gridVal=10,playableVal=14)),
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=130,gridVal=10,playableVal=15)),
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=130,gridVal=10,playableVal=16)),
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=140,gridVal=10,playableVal=14)),
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=140,gridVal=10,playableVal=15)),
    AI.ChooseMinimax(4,h.PlayableBoardHeuristic(boardVal=140,gridVal=10,playableVal=16)),
]

for i in range(0,len(minimaxPlayable)):
    for j in range(i+1,len(minimaxPlayable)):
        simulateGames(minimaxPlayable[i],minimaxPlayable[j],1000)
        

        

