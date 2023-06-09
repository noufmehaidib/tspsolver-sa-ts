# imports required libraries
from collections import deque
from TSP import *
from TS import *
import random
import math

# this class represents the Simulated Annealing algorithm.

class SA:

        def sa(no_v, adjacency_matrix, tabu_lst_size, max_no_tournmnt, ngh_strc, term_flag_1, term_flag_2, t_0, alpha):

            """
            no_v:                 number of vertices
            adjacency_matrix:     adjacency matrix
            tabu_lst_size:        number of tabu solutions in tabu_lst, here  it is always zero
            max_no_tournmnt:      number of candidates picked in tournament selection (neighbors to evalute)
            nght_stc:             neighborhood structure (swap or 2-opt)
            term_flag_1:          termination flag (inner loop)
            term_flag_2:          termination flag (outer loop)
            t_0:                  initial temperature
            alpha:                reduction factor for cooling
            """

            # initialization
            sol = list(range(no_v)) #get a permutation
            random.shuffle(sol)  # e.g. [0,1,...,no_v]
            cost = TSP.cost(no_v, adjacency_matrix, sol)
            best_sol = sol.copy()
            best_cost = cost
            tabu_lst = deque([]) #empty (not used)
            t = t_0
            result = {'cost': deque([]), 'best_cost': deque([]),
                'sol': deque([]), 'best_sol': deque([])}
            count_outer = 0

            #start outer loop
            while True:

                count_inner = 0
                best_inner_sol = sol
                best_inner_cost = cost
                #start inner loop
                while True:
                    last_sol = sol
                    last_cost = cost
                    #get a neighboring solution and its cost (ignore the tabu list since its length is zero)
                    sol, cost, tabu_lst = TSP.tournament_selection(no_v, adjacency_matrix, sol,
                                                    max_no_tournmnt, ngh_strc, tabu_lst_size,
                                                    tabu_lst, best_cost)

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
                    # (3) if not better, count++
                    else:
                        count_inner += 1

                    result['cost'].append(cost)
                    result['best_cost'].append(best_cost)
                    result['sol'].append(sol)
                    result['best_sol'].append(best_sol)

                    if count_inner > term_flag_1: #termination criteria of inner loop (equilbrium state)
                        break
                    # end of inner loop

                # update the temperature i.e. reduce it
                t = alpha * t

                # get best_inner_sol < sol
                if best_inner_cost < best_cost:
                    best_sol = best_inner_sol
                    best_cost = best_inner_cost
                    count_outer = 0 # count back zero since a better solution is found
                else:
                    count_outer += 1

                # check number of iteration
                if count_outer > term_flag_2: #termination criteria 
                   break

                # return the best solution found so far    
                return best_sol, best_cost, result
