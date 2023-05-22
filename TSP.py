# imports required libraries
from TSP import *
import random
import math

# this class represents the Travelling Salesman Problem.
class TSP:
    
    # compute cost
    def cost(no_v, adjacency_matrix, solution):
     return sum([adjacency_matrix[solution[_]][solution[(_ + 1) % no_v]] for _ in range(no_v)])
    
    # apply swap operator 
    def swap_Solution(solution, i, j):
     new_solution = solution.copy()
     new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
     return new_solution
    
    # apply 2-opt operator 
    def twoOpt_Solution(solution, i, j):
      new_solution = solution.copy()
      new_solution[i:j+1] = new_solution[i:j+1][::-1]
      return new_solution

    def delta_Swap(no_v, adjacency_matrix, solution, i, j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[j]][solution[(i + 1) % no_v]] + \
             adjacency_matrix[solution[j - 1]][solution[i]] + adjacency_matrix[solution[i]][solution[(j + 1) % no_v]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[i]][solution[(i + 1) % no_v]] - \
             adjacency_matrix[solution[j - 1]][solution[j]] - \
                 adjacency_matrix[solution[j]][solution[(j + 1) % no_v]]
     if j - i == 1 or i == 0 and j == no_v - 1:
        delta += 2 * adjacency_matrix[solution[i]
                                      ][solution[j]]  # symmetrical TSP
     return delta

    def delta_twoOpt(no_v, adjacency_matrix, solution, i, j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[i]][solution[(j + 1) % no_v]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - \
                 adjacency_matrix[solution[j]][solution[(j + 1) % no_v]]
     if i == 0 and j == no_v - 1:  # the first two value == 0, while others < 0
        delta = 0
     return delta
    
    # tournment selection for generating new solution from the neighborhood
    def tournament_selection(no_v, adjacency_matrix, solution, max_no_tournmnt, nght_stc, tabu_lst_size, tabu_lst, best_cost):
      """
      no_v:                  number of vertices
      adjacency_matrix:      adjacency matrix
      solution:              solution where the neighbours are chosen from
      max_no_tournmnt:       number of candidates picked in tournament selection (neighbors to evalute)
      nght_stc:              neighborhood structure (swap or 2-opt)
      tabu_lst_size:         number of tabu solutions in tabu_lst
      tabu_lst:              tabu moves (deque) ,out <- [...] <- in
      best_cost:             cost of the best solution
      """

      get_new_sol = nght_stc[0]
      get_delta = nght_stc[1]

      cost = TSP.cost(no_v, adjacency_matrix, solution)

      best_delta_0 = math.inf
      best_i_0 = best_j_0 = -1

      best_delta_1 = math.inf
      best_i_1 = best_j_1 = -1
      for _ in range(max_no_tournmnt):
          i, j = random.sample(range(no_v), 2)  # randomly select two indexes
          i, j = (i, j) if i < j else (j, i)  # let i < j
          vert_1, vert_2 = (solution[i], solution[j]) if solution[i] < solution[j] else (
              solution[j], solution[i])  
          delta = get_delta(no_v, adjacency_matrix, solution, i, j)
          if (vert_1, vert_2) not in tabu_lst:  # if the solution is not tabu
              if delta < best_delta_0:
                  best_delta_0 = delta
                  best_i_0 = i
                  best_j_0 = j
          else:  # If it in tabu it will be accepted if it has an improvement over the current best solution to escape from local optima
              if delta < best_delta_1:
                  best_delta_1 = delta
                  best_i_1 = i
                  best_j_1 = j
      if best_delta_1 < best_delta_0 and cost + best_delta_1 < best_cost:  # break the tabu
          vert_1, vert_2 = (solution[best_i_1], solution[best_j_1]) if solution[best_i_1] < solution[best_j_1] else (solution[best_j_1], solution[best_i_1])
          tabu_lst.remove((vert_1, vert_2))
          tabu_lst.append((vert_1, vert_2))  # move to the end of list
          
          new_sol = get_new_sol(solution, best_i_1, best_j_1)
          new_cost = cost + best_delta_1
      else:   # do not break the tabu
          if tabu_lst_size > 0: 
             if solution[best_i_0] < solution[best_j_0]:
                vert_1, vert_2 = (solution[best_i_0], solution[best_j_0]) 
             else:
              vert_1, vert_2 = (solution[best_j_0], solution[best_i_0])
              if len(tabu_lst) == tabu_lst_size: # a move in the tabu list removed if exceed tabu_tenure
                  tabu_lst.popleft()       
              tabu_lst.append((vert_1, vert_2))
        
          new_sol = get_new_sol(solution, best_i_0, best_j_0)
          new_cost = cost + best_delta_0
      return new_sol, new_cost, tabu_lst

