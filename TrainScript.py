import Model as m
import Trainer as t
import torch
import TicTacToeAI as AI
import os


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#device = torch.device('cpu')
#torch.set_num_threads(int(os.environ['SLURM_CPUS_PER_TASK']))
#torch.set_num_threads(4)

#trainer = t.Trainer()
#trainer.train(a1,a2,train_time=60)

trainer = t.Trainer(device,learning_rate = 0.01,file_name='HeuristicNetwork_SGD.pth',stat_file = "TrainingStats_SGD.csv",)
trainer.train_from_file (max_time = 42300, number_of_batches = 10,  training_file = 'training_set10.npz', validation_file = "test_set.npz")
