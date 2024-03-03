import GameState as g
import random as r
import ctypes
from abc import ABC, abstractmethod
import copy
import itertools
import Heuristics as h
import math

class Coord(ctypes.Structure):
    _fields_ = [("board",ctypes.c_ubyte),
                ("row",ctypes.c_ubyte),
                ("column",ctypes.c_ubyte)]
    
class MoveList(ctypes.Structure):
    _fields_ = [("moveNum",ctypes.c_int),
                ("moves",ctypes.POINTER(Coord))]
    
    def __init__(self,moves):
        num = len(moves)
        elems = (Coord * (num+1))()
        self.moves = ctypes.cast(elems,ctypes.POINTER(Coord))
        self.moveNum = num
        
        for i, move in enumerate(moves):
            self.moves[i].board = move[0]
            self.moves[i].row = move[1]
            self.moves[i].column = move[2]

class MCST_Args(ctypes.Structure):
    _fields_ = [("rollout",ctypes.c_int),
                ("maxRuns",ctypes.c_int),
                ("c",ctypes.c_double),
                ("threads",ctypes.c_int),
                ("shuffle",ctypes.c_bool),
                ("bias",ctypes.c_int),
                ("scale",ctypes.c_double),
                ("bias_multiplier",ctypes.c_double)]
    

    
# class MonteCarloNode(ctypes.Structure):
#     _fields_ = [("game",g.CGameState),
#                 ("parent",ctypes.pointer(MonteCarloNode)),
#                 ("possibleMoves",MoveList),
#                 ("children",ctypes.pointer((ctypes.pointer(MonteCarloNode)))),             
#                 ("move",Coord),
#                 ("childNum",ctypes.c_int),
#                 ("N",ctypes.c_double),
#                 ("T",ctypes.c_double),
#                 ("heuristic",ctypes.c_double),
#                 ("ID",ctypes.c_int)]
        

              

class TicTacToeAI:
    @abstractmethod
    def chooseMove(self,game: g.GameState):
       return
   
    @abstractmethod
    def toString(self):
        return "TicTacToeAI"
    
    def cleanUp(self):
        pass
    
    def initialize(self):
        pass

    def isWinBoard(game: g.GameState,board: int,row: int,column: int):
        if (game.board[board,row,column] != g.OPEN_VAL):
            return -2
        game.board[board,row,column] = game.currentTurn
        boardWin = game.isBoardWon(board,row,column)
        game.board[board,row,column] = 0
        return boardWin
    
    def isWinningMove(game: g.GameState,board: int,row: int,column: int):
        boardWon = TicTacToeAI.isWinBoard(game,board,row,column)
        if (boardWon == -2):
            return -2
        elif (boardWon == g.OPEN_VAL):
            return g.NO_WIN
        tempGame = copy.deepcopy(game)
        tempGame.playTurn(board,row,column)
        return tempGame.gameWon
    
    def canOpponentWinBoard(game: g.GameState,board: int,row: int,column: int):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinBoard(newGame,move[0],move[1],move[2])
            if (boardWin == g.GAME_WON):
                return g.GAME_WON
        return g.NO_WIN

    def canOpponentWin(game: g.GameState,board: int,row: int,column: int):
        newGame = copy.deepcopy(game)
        newGame.playTurn(board,row,column)
        possibleMoves = newGame.getMoves()
        for move in possibleMoves:
            boardWin = TicTacToeAI.isWinningMove(newGame,move[0],move[1],move[2])
            if (boardWin == g.GAME_WON):
                return g.GAME_WON
        return g.NO_WIN
        

class RandomAI(TicTacToeAI): 
    def chooseMove(self,game: g.GameState):
        possibleMoves = game.getMoves()
        return possibleMoves[r.randrange(len(possibleMoves))]
    
    def toString(self):
        return "RandomAI"
    
class ChooseWinLose(TicTacToeAI):
    
    def  __init__(self,priority:int,*,verbose = False):
        self.setPriority(priority)
    
    def toString(self):
        string = "ChooseWinLose:"
        count = 1
        for i in self.priority:
            if (i == 0):
                string = string + " Win Game"
            elif (i == 1):
                string = string + " Don't Lose"
            elif (i == 2):
                string = string + " Win Board"
            elif (i == 3):
                string = string + " Don't Lose Board"
            if (count != len(self.priority)):
                string = string + ","
            count = count + 1
        return string
        
        
    def setPriority(self,priority: int):
        p = (0,1,2,3)
        perm = []
        if (priority < 24):
            perm = list(itertools.permutations(p))
            self.priority = copy.deepcopy(perm[priority])
        elif (priority < 64):
            for i in range(1,len(p)):
                perm.extend(list(itertools.permutations(p, r=i)))
            self.priority = copy.deepcopy(perm[priority-24])
        else: # Invalid value - Set to default
            print("Invalid Priority - Setting to default")
            self.priority = copy.deepcopy((0,1,2,3))
    
    def chooseMove(self,game: g.GameState):
        possibleMoves = game.getMoves()
        winningMoves = []
        goodMoves = []
        otherMoves = []
        badMoves = []
        losingMoves = []
        winLoss = [0,0,0,0]
        flag = 0
        for move in possibleMoves:
            flag = 0
            if 0 in self.priority:
                winLoss[0] = ChooseWinLose.isWinningMove(game,move[0],move[1],move[2])
            if 1 in self.priority:   
                winLoss[1] = ChooseWinLose.canOpponentWin(game,move[0],move[1],move[2])
            if 2 in self.priority:
                winLoss[2] = ChooseWinLose.isWinBoard(game,move[0],move[1],move[2])
            if 3 in self.priority:
                winLoss[3] = ChooseWinLose.canOpponentWinBoard(game,move[0],move[1],move[2])
            for i in self.priority:
                if (winLoss[i] == 1):
                    if (i == 0):
                        winningMoves.append(move)
                        flag = 1
                        break
                    elif (i == 1):
                        losingMoves.append(move)
                        flag = 1
                        break
                    elif (i == 2):
                        goodMoves.append(move)
                        flag = 1
                        break
                    else:
                       badMoves.append(move)
                       flag = 1
                       break 
            if (flag == 0):
                otherMoves.append(move)
        if (len(winningMoves) > 0):
            return winningMoves[r.randrange(len(winningMoves))]        
        elif (len(goodMoves) > 0):
            return goodMoves[r.randrange(len(goodMoves))]
        elif (len(otherMoves) > 0):
            return otherMoves[r.randrange(len(otherMoves))]
        elif (len(badMoves) > 0):
            return badMoves[r.randrange(len(badMoves))]
        else:
            return losingMoves[r.randrange(len(losingMoves))]

class ChooseMinimaxPy(TicTacToeAI):
    
    VICTORY_VALUE = 1000000
    
    def  __init__(self,layers:int,heuristic:h.Heuristic,*,verbose = False):
        self.verbose = verbose
        self.layers = layers
        self.heuristic = heuristic
    
    def chooseMove(self,game:g.GameState):
        possibleMoves = game.getMoves()
        r.shuffle(possibleMoves)
        maximize = (game.currentTurn == 1)
        bestMove = 0
        bestEval = -self.VICTORY_VALUE if maximize else self.VICTORY_VALUE
        i = 0
        for move in possibleMoves:
            tempGame = copy.deepcopy(game)
            tempGame.playTurn(move[0],move[1],move[2])
            eval = self.minimax(tempGame,self.layers-1,-self.VICTORY_VALUE,self.VICTORY_VALUE,not maximize)
            if maximize and eval > bestEval:
                bestMove = i
                bestEval = eval
            elif not maximize and eval < bestEval:
                bestMove = i
                bestEval = eval
            i = i + 1
        return possibleMoves[bestMove]
    
    def toString(self):
        return "ChooseMinimaxPy: " + str(self.layers) + " Layers, " + self.heuristic.toString(self.verbose)
    
    # minimax is based on the pseudocode from https://www.youtube.com/watch?v=l-hh51ncgDI
    def minimax(self,game:g.GameState,depth:int,alpha:int,beta:int,maximize:bool):
        if game.gameWon != g.NO_WIN:
            if game.gameWon == g.GAME_WON:
                if game.currentTurn == g.X_VAL:
                    return self.VICTORY_VALUE
                else:
                    return -self.VICTORY_VALUE
            else:
                return 0
        elif depth == 0:
            return self.heuristic.heuristic(game)
        
        if maximize:
            maxEval = -self.VICTORY_VALUE 
            possibleMoves = game.getMoves()
            for move in possibleMoves:
                tempGame = copy.deepcopy(game)
                tempGame.playTurn(move[0],move[1],move[2])  
                eval = self.minimax(tempGame,depth-1,alpha,beta,False)
                maxEval = max(maxEval,eval)
                alpha = max(alpha,eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = self.VICTORY_VALUE 
            possibleMoves = game.getMoves()
            for move in possibleMoves:
                tempGame = copy.deepcopy(game)
                tempGame.playTurn(move[0],move[1],move[2])  
                eval = self.minimax(tempGame,depth-1,alpha,beta,True)
                minEval = min(minEval,eval)
                beta = min(beta,eval)
                if beta <= alpha:
                    break
            return minEval
        
class ChooseMinimax(TicTacToeAI):
    
    VICTORY_VALUE = 1000000
    
    def  __init__(self,layers:int,heuristic:h.Heuristic,*,verbose = False):
        self.verbose = verbose
        self.layers = layers
        self.heuristic = heuristic
    
    def chooseMove(self,game:g.GameState):
        possibleMoves = game.getMoves()
        r.shuffle(possibleMoves)
        maximize = (game.currentTurn == 1)
        bestMove = 0
        bestEval = -self.VICTORY_VALUE if maximize else self.VICTORY_VALUE
        i = 0
        for move in possibleMoves:
            tempGame = copy.deepcopy(game)
            tempGame.playTurn(move[0],move[1],move[2])
            eval = g.clibrary.minimaxWrapper(tempGame.toCGameState(),self.layers-1,-self.VICTORY_VALUE,self.VICTORY_VALUE,not maximize,self.heuristic.values)
            if maximize and eval > bestEval:
                bestMove = i
                bestEval = eval
            elif not maximize and eval < bestEval:
                bestMove = i
                bestEval = eval
            i = i + 1
        return possibleMoves[bestMove]
    
    def toString(self):
        return "ChooseMinimax: " + str(self.layers) + " Layers, " + self.heuristic.toString(self.verbose)
    
class MonteCarloST(TicTacToeAI):
    
    def __init__(self,max_iter,*, c = math.sqrt(2), policy = h.DEFAULT_POLICY, threads = 1,verbose = False, shuffle = True, bias = 2, scale = 0.025,multiplier=1.0):
        self.verbose = verbose
        g.clibrary.monteCarloTreeSearch.restype = Coord
        if bias < 0 or bias > 2:
            bias_val = 0
        else:
            bias_val = bias
        self.args = MCST_Args(policy,max_iter,c,threads,shuffle,bias_val,scale,multiplier)
    
    def chooseMove(self,game:g.GameState):
        coord = g.clibrary.monteCarloTreeSearch(game.toCGameState(),self.args)
        move = (coord.board,coord.row,coord.column)
        return move
    
    def toString(self):
        string = "MonteCarloST: " + str(self.args.maxRuns) + " Iterations"
        if self.verbose:
            string = string + ", c=" + str(self.args.c) +  " Policy: " + str(self.args.rollout) + " # of threads: " + str(self.args.threads) + ", Shuffle: " + str(self.args.shuffle) + ", Bias: " + str(self.args.bias) + ", Scale: " + str(self.args.scale) + ", Multiplier: " + str(self.args.bias_multiplier)
        return string
    
class MonteCarloST_SF(TicTacToeAI):
    
    def __init__(self,max_iter,*, c = math.sqrt(2), threads = 1,verbose = False, shuffle = True, bias = 2, scale = 0.025,multiplier=1.0):
        self.verbose = verbose
        g.clibrary.monteCarloTreeSearch_sf.restype = Coord
        g.clibrary.initialize.restype = (ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))
        if bias < 0 or bias > 2:
            bias_val = 0
        else:
            bias_val = bias
        self.args = MCST_Args(h.DEFAULT_POLICY,max_iter,c,1,True,2,scale,multiplier)
    
    def chooseMove(self,game:g.GameState):
        coord = g.clibrary.monteCarloTreeSearch_sf(game.toCGameState(),self.args,self.root)
        move = (coord.board,coord.row,coord.column)
        return move
    
    def toString(self):
        string = "MonteCarloST_SF: " + str(self.args.maxRuns) + " Iterations"
        if self.verbose:
            string = string + ", c=" + str(self.args.c) + ", Scale: " + str(self.args.scale) + ", Multiplier: " + str(self.args.bias_multiplier)
        return string
    
    def initialize(self):
        self.root = g.clibrary.initialize()
        
    def cleanUp(self):
        g.clibrary.freeTree(self.root)
        
    
    
    
class MonteCarloSTPy(TicTacToeAI):
    
    def __init__(self,max_iter,*, c = math.sqrt(2),verbose = False):
        self.verbose = verbose
        self.max_iter = max_iter
        self.c = c
    
    def chooseMove(self,game:g.GameState):
        root = Node(game,None,None)
        root.expand()
        for i in range(0,self.max_iter):
            leaf = root.traverse(self.c)
            result = leaf.rollout(root.game.currentTurn)
            leaf.backpropogate(result)
        
        best_score = -float('inf')
        best = 0
        for (i,child) in enumerate(root.children):
            if child.N > 0:
                score = child.T / child.N
            else:
                score = 0
            if score > best_score:
                best = i
                best_score = score
        
        return root.children[best].move
    
    def toString(self):
        return "MonteCarloSTPy: " + str(self.max_iter) + " Iterations, c=" + str(self.c)
                
            
    
class Node:
    
    def __init__(self,game,parent,move):
        
        self.T = 0
        self.N = 0
        
        self.parent = parent
        
        self.game = copy.deepcopy(game)
        if move is not None:
            self.game.playTurn(move[0],move[1],move[2])
        
        self.move = move
        
        if self.game.gameWon == g.NO_WIN:
            self.possibleMoves = self.game.getMoves()
            r.shuffle(self.possibleMoves)
        else:
            self.possibleMoves = []

        self.children = []
        
    def traverse(self,c):        
        if len(self.children) == 0:
            if self.N == 0 or len(self.possibleMoves) == 0 :
                return self
            self.expand()
            return self.children[0]
        
        best_ucb = -float('inf')
        best = -1
        ucb = -float('inf')
        for (i,child) in enumerate(self.children):
            ucb = child.calcUCB(c)
            if ucb > best_ucb :
                best = i
                best_ucb = ucb
                
        return self.children[best].traverse(c)            
        
    def calcUCB(self,c):
        if self.N == 0:
            return float('inf')
        parent = self.parent
        if parent is None:
            parent = self
        return (self.T / self.N) + c * math.sqrt(math.log(self.parent.N) / self.N)
        
    def rollout(self,player):
        random = RandomAI()
        game = copy.deepcopy(self.game)
        while game.gameWon == g.NO_WIN:
            move = random.chooseMove(game)
            game.playTurn(move[0],move[1],move[2])
        
        if game.gameWon == g.STALEMATE:
            return (1/2)
        
        if game.currentTurn == player:
            return 1
        
        return 0
        
    def expand(self):
        for move in self.possibleMoves:
            self.children.append(Node(self.game,self,move))
    
    def backpropogate(self,result):
        self.N += 1
        self.T += result
        
        if self.parent is None:
            return
        
        self.parent.backpropogate(result)
        
        
            