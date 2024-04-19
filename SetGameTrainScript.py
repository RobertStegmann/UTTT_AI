import Model as m
import SetGameTrainer as t
import torch
import TicTacToeAI as AI

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

a1 = AI.MonteCarloST(1000)
a2 = AI.MonteCarloST(1000)

#trainer = t.Trainer()
#trainer.train(a1,a2,train_time=60)

trainer = t.SetGameTrainer(stat_file = "SGS_100Games_2.csv")
trainer.train(a1,a2,sampleSize = 200,epochs = 20,max_boards=2)