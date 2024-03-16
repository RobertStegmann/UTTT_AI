import Model as m
import Trainer as t
import torch
import TicTacToeAI as AI

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

a1 = AI.MonteCarloST(1000)
a2 = AI.MonteCarloST(1000)

trainer = t.Trainer()
trainer.train(a1,a2,train_time=60)