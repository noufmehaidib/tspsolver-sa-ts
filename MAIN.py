#imports required libraries

import matplotlib.pyplot as plt
from pprint import pprint
from tqdm import tqdm
import numpy as np
from TSP import *
from SA import *
import random
import time
import math
import TS
import os

class MAIN:

        # make directoy for the result, if not found
        if not os.path.exists('results'):
            os.makedirs('results')

        # load tsp_38 file 
        # pos = [[float(x) for x in s.split()[1:]] for s in open('data/dj38.txt').readlines()]
        # n = len(pos)

        # load qa194 file
        pos = [[float(x) for x in s.split()[1:]] for s in open('data/qa194.txt').readlines()]
        n = len(pos)

        # calculate adjacency matrix
        adj_mat = np.zeros([n, n]) #initialize all values to zero1es
        for i in range(n):
            for j in range(i, n):
                adj_mat[i][j] = adj_mat[j][i] = np.linalg.norm(np.subtract(pos[i], pos[j]))

        # initialization
        #opt_cost = 6656  # opt for the tsp_38
        opt_cost = 9352  # opt for the qa194
        num_tests = 100
        result = {'best_sol': [], 'best_cost': math.inf, 'best_gap': math.inf,
                  'cost': [0] * num_tests, 'time': [0] * num_tests,
                  'avg_cost': math.inf, 'avg_time': math.inf,
                  'min_cost': math.inf, 'min_time': math.inf,
                  'max_cost': math.inf, 'max_time': math.inf}

        best_cost = math.inf
        best_sol = []
        data = {}

        # welcome message
        print("####WELCOME TO TSP SOLVER####")

        # set both algorithm and operator method
        algorithm = '1'
        operator = '2'

        while algorithm != '3' or operator != '3':
            # choice of algorithm
            print("####PLEASE CHOOSE WHICH ALGORITHM YOU WOULD LIKE TO USE####")
            algorithm = input("#### 1: SIMULATED ANNEALING, 2: TABU SEARCH, 3: EXIT ####")

            if algorithm == '3':
                break

            # choice of neighborhood structure
            print("####PLEASE CHOOSE WHICH NEIGHBORHOOD STRUCTURE YOU WOULD LIKE TO USE####")
            operator = input("#### 1: SWAP, 2: 2-OPT, 3: EXIT ####")

            # Swap
            if operator == '1':
               ngh_strc = [TSP.swap_Solution, TSP.delta_Swap]
            # 2-opt
            elif operator == '2':
                ngh_strc = [TSP.twoOpt_Solution, TSP.delta_twoOpt]
            # not a valid choice (run the application again to start)
            else:
                break
            #the initial temperature and the reduction factor are randomly generated
            #since there is lots of randomness, print t_0 and alpha to be used later on to compare the results:
            t_0=random.randint(100,1000)
            alpha=random.random()
            print("The initial temperature is: ",t_0)
            print("The reduction factor is:", alpha)

            for _ in tqdm(range(num_tests)):
                #start time
                start = time.time()

                # SA Algorithm
                if algorithm == '1':
                   algorithm_name = 'Simulated Anealing'
                   best_sol, best_cost, data = SA.sa(n,adj_mat=adj_mat,tb_size = 0,max_tnm=100,ngh_strc=ngh_strc,term_flag_1 =25, term_flag_2=200,t_0=t_0,alpha=alpha)

                # TS Algorithm
                elif algorithm == '2':
                    algorithm_name = 'Tabu Search'
                    best_sol, best_cost, data = TS.ts(n, adj_mat=adj_mat,
                                          tb_size=25,  # tabu solutions in tb_list
                                          max_tnm=100,  # how many candidates picked in tournament selection
                                          ngh_strc=ngh_strc,  # [get_sol, get delta], method of mutation, e.g. swap, 2-opt
                                          term_count=200  # terminate threshold if best_cost nor change
                                          )

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
                   result['best_gap'] = best_cost / opt_cost - 1

            # save figure in results dir
            plt.plot(range(len(data['cost'])), data['cost'], color='b', alpha=math.pow(num_tests, -0.75))
            plt.plot(range(len(data['cost'])), data['best_cost'], color='r', alpha=math.pow(num_tests, -0.75))
            plt.title('Solving TSP with {}'.format(algorithm_name))
            plt.xlabel('Number of Iteration')
            plt.ylabel('Cost')
            plt.savefig('results/{}.png'.format(algorithm))

            # update results
            #avg
            result['avg_cost'] = np.mean(result['cost'])
            result['avg_time'] = np.mean(result['time'])
            
            #max
            result['max_cost'] = np.max(result['cost'])
            result['max_time'] = np.max(result['time'])
            
            #min
            result['min_cost'] = np.min(result['cost'])
            result['min_time'] = np.min(result['time'])
            
            # print results
            print('best_sol',result['best_sol'])
            print('best_cost',result['best_cost'])
            print('best_gap',result['best_gap'])
            print('time',result['time'][_])

            print('avg_cost',result['avg_cost'])
            print('avg_time',result['avg_time'])

            print('min_cost',result['min_cost'])
            print('min_time',result['min_time'])

            print('max_cost',result['max_cost'])
            print('max_time',result['max_time'])