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
    

#monteAI_rand = AI.MonteCarloST(5000,policy=0,verbose=True)
#monteAI_chooseWin = AI.MonteCarloST(2500,policy=1,verbose=True)
# monteAI_chooseWin_low = AI.MonteCarloST(1000,policy=1,verbose=True)
# monteAI_chooseWin_lower = AI.MonteCarloST(500,policy=1,verbose=True)



# simulateGames(monteAI_rand,monteAI_chooseWin_low,1000)
# simulateGames(monteAI_rand,monteAI_chooseWin_lower,1000)

# simulateGames(monteAI_chooseWin,monteAI_chooseWin_low,1000)
# simulateGames(monteAI_chooseWin,monteAI_chooseWin_lower,1000)
# simulateGames(monteAI_chooseWin_low,monteAI_chooseWin_lower,1000)

monteAI_nothread = AI.MonteCarloST(2000,threads = 1,verbose=True)
monteAI_threads_same_rollout = [
                   AI.MonteCarloST(3000,threads = 2,verbose=True),
                   AI.MonteCarloST(2000,threads = 3,verbose=True),
                   AI.MonteCarloST(1500,threads = 4,verbose=True),
                   ]

monteAI_threads_same_iteration = [AI.MonteCarloST(6000,threads = 2,verbose=True),
                   AI.MonteCarloST(6000,threads = 3,verbose=True),
                   AI.MonteCarloST(6000,threads = 4,verbose=True),
                   ]
minimax_monte = AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=600,threads=1))

minimax_monte_thread = [AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=600,threads=2),verbose=True),
                        AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=600,threads=3),verbose=True), 
                        AI.ChooseMinimax(2,h.MonteCarloHeuristic(maxRuns=600,threads=4),verbose=True)
                    ]
for ai in minimax_monte_thread:
    simulateGames(ai,minimax_monte,500)

# for ai in monteAI_threads_same_rollout:
#     simulateGames(ai,monteAI_nothread,500)
    
#for ai in monteAI_threads_same_iteration:
#    simulateGames(ai,monteAI_nothread,500)
         
# for ai in monteHeurAI_winLose:
#     simulateGames(ai,monteHeurAI_rand,500)
#     for ai_2 in monteHeurAI_win:
#         simulateGames(ai,ai_2,500)

# minimax1 = AI.ChooseMinimax(4,h.StaticHeuristic())
# minimax2 = AI.ChooseMinimax(4,h.PlayableBoardHeuristic())

# simulateGames(minimax1,minimax2,1000)        

