import random
import math
from collections import deque
#from tsp import get_cost

def tnm_selection(no_v, adj_mat, sol, max_tnm, nght_stc, tb_size, tb_list, fq_dict, best_cost):
    """
    :param no_v: number of vertices
    :param adj_mat: adjacency matrix
    :param sol: solution where the neighbours are chosen from
    :param max_tnm: how many candidates picked in tournament selection
    :param nght_stc: [get_sol, get delta], method of mutation, e.g. swap, 2-opt
    :param tb_size: >=0, max length of tb_list
    :param tb_list: deque ,out <- [...] <- in
    :param fq_dict: visit times of vertex pair (not used!)
    :param best_cost: cost of the best solution
    """

    get_new_sol = nght_stc[0]
    get_delta = nght_stc[1]

    cost = get_cost(no_v, adj_mat, sol)

    best_delta_0 = math.inf
    best_i_0 = best_j_0 = -1

    best_delta_1 = math.inf
    best_i_1 = best_j_1 = -1
    for _ in range(max_tnm):
        i, j = random.sample(range(no_v), 2)   # randomly select two indexes
        i, j = (i, j) if i < j else (j, i)  # let i < j
        v_1, v_2 = (sol[i], sol[j]) if sol[i] < sol[j] else (
            sol[j], sol[i])                 # v_1 < v_2 make indexing in tb_list and fq_dict convenient
        delta = get_delta(no_v, adj_mat, sol, i, j)
        if (v_1, v_2) not in tb_list:       # if not tabu
            if delta < best_delta_0:
                best_delta_0 = delta
                best_i_0 = i
                best_j_0 = j
        else:  # if tabu
            if delta < best_delta_1:
                best_delta_1 = delta
                best_i_1 = i
                best_j_1 = j
    if best_delta_1 < best_delta_0 and cost + best_delta_1 < best_cost:  # break the tabu
        v_1, v_2 = (sol[best_i_1], sol[best_j_1]) if sol[best_i_1] < sol[best_j_1] else (sol[best_j_1], sol[best_i_1])
        tb_list.remove((v_1, v_2))
        tb_list.append((v_1, v_2))  # move to the end of list
        fq_dict[(v_1, v_2)] = fq_dict.get((v_1, v_2), 0) + 1
        new_sol = get_new_sol(sol, best_i_1, best_j_1)
        new_cost = cost + best_delta_1
    else:  # do not break the tabu
        if tb_size > 0:
            v_1, v_2 = (sol[best_i_0], sol[best_j_0]) \
                if sol[best_i_0] < sol[best_j_0] \
                else (sol[best_j_0], sol[best_i_0])
            if len(tb_list) == tb_size:
                tb_list.popleft()
            tb_list.append((v_1, v_2))
            fq_dict[(v_1, v_2)] = fq_dict.get((v_1, v_2), 0) + 1
        new_sol = get_new_sol(sol, best_i_0, best_j_0)
        new_cost = cost + best_delta_0
    # assert abs(new_cost - get_cost(n, adj_mat, new_sol)) < 1e-9, 'new_sol does not match new_cost'
    return new_sol, new_cost, tb_list, fq_dict


def ts(no_v, adj_mat, tb_size, max_tnm, nght_stc, term_count):

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
    tb_list = deque([])
    fq_dict = {}
    best_sol = sol.copy()
    best_cost = get_cost(no_v, adj_mat, sol)
    result = {'cost': deque([]), 'best_cost': deque([])}
    count = 0

    ###
    while True:
        sol, cost, tb_list, fq_dict = tnm_selection(no_v, adj_mat, sol,
                                                    max_tnm, nght_stc, tb_size,
                                                    tb_list, fq_dict, best_cost)
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