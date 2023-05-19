#imports required libraries

from collections import deque
#from tb import tnm_selection
#from tsp import get_cost
import random
import math

def sa(n, adj_mat, tb_size, max_tnm, ngh_strc, term_flag_1, term_flag_2, t_0, alpha):
    
    """
    n: number of vertices
    adj_mat: adjacency matrix
    tb_size: max length of tb_list, here in sa it is always zero
    max_tnm: candidates picked in tournament selection
    nght_stc: neighborhood structure
    term_flag_1: termination flag (inner loop)
    term_flag_2: termination flag (outer loop)
    t_0: initial temperature
    alpha: reduction factor for cooling
    """

    # initialization  
    sol = list(range(n)) #get a permutation 
    random.shuffle(sol)  # e.g. [0,1,...,n]
    cost = get_cost(n, adj_mat, sol) 
    best_sol = sol.copy()
    best_cost = cost
    tb_list = deque([]) #empty (not used)
    fq_dict = {}  #empty (not used)
    t = t_0
    result = {'cost': deque([]), 'best_cost': deque([]),
            'sol': deque([]), 'best_sol': deque([])}
    count_outer = 0

    #since there is lots of randomness, print t_0 and alpha to be used later on to compare the results:
    print("The initial temperature is:" + t_0)
    print("The reduction factor is:" + alpha)

    #start outer loop
    while True:
        count_inner = 0
        best_inner_sol = sol
        best_inner_cost = cost
        #start inner loop
        while True:
            last_sol = sol
            last_cost = cost

            #get a neighboring solution
            sol, cost, tb_list, fq_dict = tnm_selection(n, adj_mat, sol,
                                                        max_tnm, ngh_strc, tb_size,
                                                        tb_list, fq_dict, best_cost)
            
            # update the solution 
            # (1) if the new solution is worse (it can be accepted with a random propability)
            if cost > last_cost and math.exp((last_cost - cost) / t) < random.random(): #random float number [0,1]
                sol = last_sol
                cost = last_cost
            # (2) if the new solution is better (always accept)
            if cost < best_inner_cost:
                best_inner_sol = sol
                best_inner_cost = cost
                count_inner = 0  # count back zero (for equilibrium state)
            # (3) if the new solution is worse and not accpeted in the (1) condition
            else:
                count_inner += 1

            result['cost'].append(cost)
            result['best_cost'].append(best_cost)
            result['sol'].append(sol)
            result['best_sol'].append(best_sol)

            if count_inner > term_flag_1:
                break
            # end of inner loop
        
        # update the temperature i.e. reduce it
        t = alpha * t 

        # get best_inner_sol < sol
        if best_inner_cost < best_cost:
            best_sol = best_inner_sol
            best_cost = best_inner_cost
            count_2 = 0 # count back zero since a better solution is found
        else:
            count_2 += 1
        
        # check number of iteration
        if count_2 > term_flag_2:
            break
    
    result['fq_dict'] = fq_dict
    return best_sol, best_cost, result
