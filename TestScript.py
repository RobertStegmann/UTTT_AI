import Model as m
import Trainer as t
import torch
import TicTacToeAI as AI
import os

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

device = torch.device('cpu')
#torch.set_num_threads(int(os.environ['SLURM_CPUS_PER_TASK']))

#a1 = AI.MonteCarloST(1000)
#a2 = AI.MonteCarloST(1000)

#trainer = t.Trainer()
#trainer.train(a1,a2,train_time=60)

t.Trainer.dataset_shape("training_set_15moves.npz")
t.Trainer.dataset_shape("training_set_20moves.npz")

#trainer = t.Trainer(device,learning_rate=0.001,file_name='HeuristicNetwork_test.pth',stat_file = "TrainingStats_test.csv",)
#trainer.train(a1,a2,train_time = 600,max_boards = 2)