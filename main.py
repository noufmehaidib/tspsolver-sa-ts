#imports required libraries
# from travellingSalesManProblem import *
import matplotlib.pyplot as plt
from pprint import pprint
import simulatedAnnealing
from tqdm import tqdm
# import tabuSearch
import numpy as np
import random
import time
import math
import os

# make directoy for the result, if not found
if not os.path.exists('results'):
    os.makedirs('results')

# load tsp_38 file 
pos = [[float(x) for x in s.split()[1:]] for s in open('data/tsp_38.txt').readlines()]
n = len(pos)

# calculate adjacency matrix
adj_mat = np.zeros([n, n]) #initialize all values to zeroes
for i in range(n):
    for j in range(i, n):
        adj_mat[i][j] = adj_mat[j][i] = np.linalg.norm(np.subtract(pos[i], pos[j]))

# initialization 
opt_cost = 6659.439330623091  # got the result from tsp_gurobi.py
num_tests = 100  
result = {'best_sol': [], 'best_cost': math.inf,
          'cost': [0] * num_tests, 'time': [0] * num_tests,
          'avg_cost': math.inf, 'avg_time': math.inf, 
          'min_cost': math.inf, 'min_time': math.inf, 
          'max_cost': math.inf, 'max_time': math.inf     }
best_cost = math.inf
best_sol = []
data = {}

# welcome message 
print("####WELCOME TO TSP SOLVER####")

# set both algorithm and operator method
algorithm = ''
operator == ''

while algorithm != '3' or operator != '3':
    # choice of algorithm
    print("####PLEASE CHOOSE WHICH ALGORITHM YOU WOULD LIKE TO USE####")
    algorithm = input("#### 1: SIMULATED ANNEALING, 2: TABU SEARCH, 3: EXIT ####")
    
    # choice of neighborhood structure
    print("####PLEASE CHOOSE WHICH NEIGHBORHOOD STRUCTURE YOU WOULD LIKE TO USE####")
    operator = input("#### 1: SWAP, 2: 2-OPT, 3: EXIT ####")

    # Swap
    if operator == '1':
       ngh_strc = [get_new_sol_swap, get_delta_swap]
    # 2-opt   
    elif operator == '2':
        ngh_strc = [get_new_sol_2opt, get_delta_2opt]
    # not a valid choice (run the application again to start)
    else:
        break

    for _ in tqdm(range(num_tests)):
        #start time
        start = time.time()

        # SA Algorithm
        if algorithm == '1':
           algorithm_name = 'Simulated Anealing'
           #the initial temperature and the reduction factor are randomly generated
           best_sol, best_cost, data = simulatedAnnealing.sa(n=n,adj_mat=adj_mat, tb_size = 0, max_tnm=20,ngh_strc=ngh_strc,term_flag_1=25,term_flag_2=25,t_0=random.radiant(100,1000),alpha=random.random()) 
        
        # TS Algorithm
        elif algorithm == '2':
            algorithm_name = 'Tabu Search'

        # not a valid choice (run the application again to start)
        else:
            break 
        
        #end time
        end = time.time()
        result['time'][_] = end - start
        result['cost'][_] = best_cost
        if best_cost < result['best_cost']:
           result['best_sol'] = best_sol
           result['best_cost'] = best_cost

        # save figure in results dir
        plt.plot(range(len(data['cost'])), data['cost'], color='b', alpha=math.pow(num_tests, -0.75))
        plt.plot(range(len(data['cost'])), data['best_cost'], color='r', alpha=math.pow(num_tests, -0.75))
        plt.title('Solving TSP with {}'.format(algorithm_name))
        plt.xlabel('Number of Iteration')
        plt.ylabel('Cost')
        plt.savefig('results/{}.png'.format(algorithm))

        # print results
        result['avg_cost'] = np.mean(result['cost'])
        result['avg_time'] = np.mean(result['time'])
        result['max_cost'] = np.max(result['cost'])
        result['max_time'] = np.max(result['time'])
        result['min_cost'] = np.min(result['cost'])
        result['min_time'] = np.min(result['time'])

        pprint(result)
