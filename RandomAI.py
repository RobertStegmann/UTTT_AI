import GameState as g
import random as r

class RandomAI:
    
    def chooseMove(game):
        if game.currentBoard == 9:
            possibleMoves = game.chooseMoveFullBoard()
        else:
            possibleMoves = game.chooseMoveSingleGrid()
        return possibleMoves[r.randrange(len(possibleMoves))]       
    
          
