import random
import math
from collections import deque
from TSP import *


def ts(no_v, adj_mat, tb_size, max_tnm, nght_stc, term_count,tabu_tenure):

    """
    no_v:       number of vertices
    adj_mat:    adjacency matrix
    tb_size:    tabu solutions in tb_list
    max_tnm:    how many candidates picked in tournament selection
    nght_stc:   neighborhood structure (swap or 2-opt)
    term_count: termination flag
    """
    # initialization
    sol = list(range(no_v))
    random.shuffle(sol)  # e.g. [0,1,...,n]
    tb_list = deque()
    fq_dict = {}
    best_sol = sol.copy()
    best_cost = cost(no_v, adj_mat, sol)
    result = {'cost': deque([]), 'best_cost': deque([])}
    count = 0

    ###
    while True:
        sol, cost, tb_list, fq_dict = tnm_selection(no_v, adj_mat, sol,
                                                    max_tnm, nght_stc, tb_size,
                                                    tb_list, fq_dict, best_cost,tabu_tenure)
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
    result['fq_dict'] = fq_dict
    return best_sol, best_cost, result
