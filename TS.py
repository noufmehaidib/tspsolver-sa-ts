# imports required libraries
from collections import deque
from TSP import *
import random

# this class represents Tabu Search algorithm.
class TS:
    
        def ts(no_v, adjacency_matrix, tabu_lst_size, max_no_tournmnt, ngh_strc, term_flag):

            """
            no_v:                number of vertices
            adjacency_matrix:    adjacency matrix
            tabu_lst_size:       number of tabu solutions in tabu_lst
            max_no_tournmnt:     number of candidates picked in tournament selection (neighbors to evalute)
            ngh_strc:            neighborhood structure (swap or 2-opt)
            term_flag:           termination flag
            """
            # initialization
            sol = list(range(no_v)) #get a permutation
            random.shuffle(sol)  # e.g. [0,1,...,no_v]
            tabu_lst = deque([])
            
            best_sol = sol.copy()
            best_cost = TSP.cost(no_v, adjacency_matrix, sol)
            result = {'cost': deque([]), 'best_cost': deque([])}
            count = 0

            # start loop
            while True:
                #get a neighboring solution and its cost, update the tabu list
                sol, cost, tabu_lst = TSP.tournament_selection(no_v, adjacency_matrix, sol,
                                                            max_no_tournmnt, ngh_strc, tabu_lst_size,
                                                            tabu_lst, best_cost)
                
                # (1) if the new solution is better (always accept)
                if cost < best_cost:
                    best_sol = sol
                    best_cost = cost
                    count = 0 
                # (2) if not better, count++
                else: #else
                    count += 1

                result['cost'].append(cost)
                result['best_cost'].append(best_cost)

                # check number of iteration
                if count > term_flag: #termination criteria 
                    break

            # return the best solution found so far     
            return best_sol, best_cost, result

