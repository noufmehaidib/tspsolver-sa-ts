# imports required libraries
from tqdm import tqdm
import numpy as np
from TSP import *
from SA import *
from TS import *
import random
import time
import math

# this class is responsible for starting the program.

class MAIN:
        
        # welcome message
        print("####WELCOME TO TSP SOLVER####")

        # load dj38 file 
        # file_distance = [[float(x) for x in s.split()[1:]] for s in open('data/dj38.txt').readlines()]
        # no_v = len(file_distance)

        # load qa194 file
        file_distance = [[float(x) for x in s.split()[1:]] for s in open('data/qa194.txt').readlines()]
        no_v = len(file_distance)


        # initialization
        #opt_cost = 6659.43 # opt for the dj38 solved in guroby.py
        opt_cost = 9352  # opt for the qa194 solved in guroby.py
        num_tests = 100 #this is for tqdm loop
        result = {'best_sol': [], 'best_cost': math.inf, 'best_gap': math.inf,
                  'cost': [0] * num_tests, 'time': [0] * num_tests,
                  'avg_cost': math.inf, 'avg_time': math.inf,
                  'min_cost': math.inf, 'min_time': math.inf,
                  'max_cost': math.inf, 'max_time': math.inf}
        best_cost = math.inf
        best_sol = []
        data = {}

        # calculate adjacency matrix
        adjacency_matrix = np.zeros([no_v, no_v]) #initialize all values to zero1es
        for i in range(no_v):
            for j in range(i, no_v):
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = np.linalg.norm(np.subtract(file_distance[i], file_distance[j]))

        # let the user choose the prefered algorithm (SA or TS) + operator (Swap or 2-opt)

        # choice of algorithm
        algorithm = ''
        print("####PLEASE CHOOSE WHICH ALGORITHM YOU WOULD LIKE TO USE####")
        algorithm = input("#### 1: SIMULATED ANNEALING, 2: TABU SEARCH####")

        # if the chosen algorithm is SA,the initial temperature (t_0) and the reduction factor (alpha) are randomly generated
        # print t_0 and alpha to be used later on to compare the results:
        if algorithm == '1':
            t_0=random.randint(1000,5000)
            alpha=random.random()
            print("The initial temperature is: ",t_0)
            print("The reduction factor is:", alpha)

        # choice of neighborhood structure
        operator = ''
        print("####PLEASE CHOOSE WHICH NEIGHBORHOOD STRUCTURE YOU WOULD LIKE TO USE####")
        operator = input("#### 1: SWAP, 2: 2-OPT ####")

        # swap
        if operator == '1':
            operator_name = 'Swap Operator'
            ngh_strc = [TSP.swap_Solution, TSP.delta_Swap]
        # 2-opt
        elif operator == '2':
            operator_name = '2-opt Operator'
            ngh_strc = [TSP.twoOpt_Solution, TSP.delta_twoOpt]
        # not a valid choice (run the application again to start)
        else:
            exit
        
        # start searching
        # start time of search
        start = time.time()
        for _ in tqdm(range(num_tests)):    
            # SA Algorithm
            if algorithm == '1':
                algorithm_name = 'Simulated Anealing'
                best_sol, best_cost, data = SA.sa(no_v,adjacency_matrix,tabu_lst_size=0,max_no_tournmnt=100,ngh_strc=ngh_strc,term_flag_1=50, term_flag_2=1000,t_0=t_0,alpha=alpha)

            # TS Algorithm
            elif algorithm == '2':
                 algorithm_name = 'Tabu Search'
                 best_sol, best_cost, data = TS.ts(no_v,adjacency_matrix,tabu_lst_size=25,max_no_tournmnt=100,ngh_strc=ngh_strc,term_flag=1000)

            # not a valid choice (run the application again to start)
            else:
                exit

            # end serach time
            end = time.time()
            result['time'][_] = end - start
            result['cost'][_] = best_cost
            if best_cost < result['best_cost']:
                result['best_sol'] = best_sol
                result['best_cost'] = best_cost
                result['best_gap'] = best_cost / opt_cost - 1

        # update results
        # avg
        result['avg_cost'] = np.mean(result['cost'])
        result['avg_time'] = np.mean(result['time'])
            
        # max
        result['max_cost'] = np.max(result['cost'])
        result['max_time'] = np.max(result['time'])
            
        # min
        result['min_cost'] = np.min(result['cost'])
        result['min_time'] = np.min(result['time'])
            
        # print results
        print('Search using ' + algorithm_name + 'and' + operator_name)
        print('best_sol',result['best_sol'])
        print('best_cost',result['best_cost'])
        #print('best_gap',result['best_gap'])
        print('time',result['time'][_])

        # print('avg_cost',result['avg_cost'])
        # print('avg_time',result['avg_time'])

        # print('min_cost',result['min_cost'])
        # print('min_time',result['min_time'])

        # print('max_cost',result['max_cost'])
        # print('max_time',result['max_time'])