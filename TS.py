import random
import math
from collections import deque
from TSP import *


def ts(no_v, adj_mat, tb_size, max_tnm, ngh_strc, term_count):

    """
    no_v:       number of vertices
    adj_mat:    adjacency matrix
    tb_size:    tabu solutions in tb_list
    max_tnm:    how many candidates picked in tournament selection
    ngh_strc:   neighborhood structure (swap or 2-opt)
    term_count: termination flag
    """
    # initialization
    sol = list(range(no_v))
    random.shuffle(sol)  # e.g. [0,1,...,n]
    tb_list = deque([])
    
    best_sol = sol.copy()
    best_cost = TSP.cost(no_v, adj_mat, sol)
    result = {'cost': deque([]), 'best_cost': deque([])}
    count = 0

    ###
    while True:

        sol, cost, tb_list, fq_dict = TSP.tnm_selection(no_v, adj_mat, sol,
                                                    max_tnm, ngh_strc, tb_size,
                                                    tb_list, best_cost)
        # mention the iteratively variable 'sol'
        if cost < best_cost:
            best_sol = sol
            best_cost = cost
            count = 0
        else:
            count += 1
        result['cost'].append(cost)
        result['best_cost'].append(best_cost)
        if count > term_count:
            break
    return best_sol, best_cost, result

