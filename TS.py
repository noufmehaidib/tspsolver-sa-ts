from collections import deque
from TSP import *
import random


class TS:
    
        def ts(no_v, adjacency_matrix, tabu_lst_size, max_no_tournmnt, ngh_strc, term_flag):

            """
            no_v:       number of vertices
            adjacency_matrix:    adjacency matrix
            tabu_lst_size:    number of tabu solutions in tabu_lst
            max_no_tournmnt:    number of candidates picked in tournament selection (neighbors to evalute)
            ngh_strc:   neighborhood structure (swap or 2-opt)
            term_flag: termination flag
            """
            # initialization
            sol = list(range(no_v))
            random.shuffle(sol)  # e.g. [0,1,...,no_v]
            tabu_lst = deque([])
            
            best_sol = sol.copy()
            best_cost = TSP.cost(no_v, adjacency_matrix, sol)
            result = {'cost': deque([]), 'best_cost': deque([])}
            count = 0

            ###
            while True:

                sol, cost, tabu_lst = TSP.tnm_selection(no_v, adjacency_matrix, sol,
                                                            max_no_tournmnt, ngh_strc, tabu_lst_size,
                                                            tabu_lst, best_cost)
                # mention the iteratively variable 'sol'
                if cost < best_cost:
                    best_sol = sol
                    best_cost = cost
                    count = 0
                else:
                    count += 1
                result['cost'].append(cost)
                result['best_cost'].append(best_cost)
                if count > term_flag:
                    break
            return best_sol, best_cost, result

