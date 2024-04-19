import Model as m
import Trainer as t
import torch
import TicTacToeAI as AI
import os

device = torch.device('cpu')

a1 = AI.MonteCarloST(2000)
a2 = AI.MonteCarloST(2000)


#trainer = t.Trainer()
#trainer.train(a1,a2,train_time=60)

trainer = t.Trainer(device)

#trainer.generate_dataset(a1,a2,max_games=2000,max_boards = 2,file_name="training_set.npz")
#trainer.generate_dataset(a1,a2,max_games=1000,max_boards = 4,file_name="training_set.npz")
#trainer.generate_dataset(a1,a2,max_games=500,max_boards = 8,file_name="training_set.npz")
#trainer.generate_dataset(a1,a2,max_games=50,max_boards = 10,file_name="training_set.npz")
#trainer.generate_dataset(a1,a2,max_games=153,max_boards = 82,file_name="ts_full_games.npz")

t.Trainer.merge_dataset("training_set.npz","training_set_10moves.npz","large_set.npz")
t.Trainer.merge_dataset("large_set.npz","training_set_15moves.npz","large_set.npz")
t.Trainer.merge_dataset("large_set.npz","training_set_20moves.npz","large_set.npz")
t.Trainer.merge_dataset("large_set.npz","ts_full_games.npz","full_set.npz")
