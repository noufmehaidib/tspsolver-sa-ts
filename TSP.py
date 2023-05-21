import random
import math
from collections import deque


class TSP:

    def cost(n, adjacency_matrix, solution):
     return sum([adjacency_matrix[solution[_]][solution[(_ + 1) % n]] for _ in range(n)])

    def swap_Solution(solution, i, j):
     new_solution = solution.copy()
     new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
     return new_solution

    def twoOpt_Solution(solution, i, j):
      new_solution = solution.copy()
      new_solution[i:j+1] = new_solution[i:j+1][::-1]
      return new_solution

    def delta_Swap(n, adjacency_matrix, solution, i, j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[j]][solution[(i + 1) % n]] + \
             adjacency_matrix[solution[j - 1]][solution[i]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[i]][solution[(i + 1) % n]] - \
             adjacency_matrix[solution[j - 1]][solution[j]] - \
                 adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if j - i == 1 or i == 0 and j == n - 1:
        delta += 2 * adjacency_matrix[solution[i]
                                      ][solution[j]]  # symmetrical TSP
     return delta

    def delta_twoOpt(n, adjacency_matrix, solution, i, j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - \
                 adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if i == 0 and j == n - 1:  # the first two value == 0, while others < 0
        delta = 0
     return delta

    def tnm_selection(no_v, adj_mat, sol, max_tnm, nght_stc, tb_size, tb_list, best_cost):
      """
      :param n: number of vertices
      :param adj_mat: adjacency matrix
      :param sol: solution where the neighbours are chosen from
      :param max_tnm: how many candidates picked in tournament selection
      :param nght_stc: [get_sol, get delta], method of mutation, e.g. swap, 2-opt
      :param tb_size: >=0, max length of tb_list
      :param tb_list: deque ,out <- [...] <- in
      :param best_cost: cost of the best solution
      """

      get_new_sol = nght_stc[0]
      get_delta = nght_stc[1]

      cost = TSP.cost(no_v, adj_mat, sol)

      best_delta_0 = math.inf
      best_i_0 = best_j_0 = -1

      best_delta_1 = math.inf
      best_i_1 = best_j_1 = -1
      for _ in range(max_tnm):
          i, j = random.sample(range(no_v), 2)  # randomly select two indexes
          i, j = (i, j) if i < j else (j, i)  # let i < j
          v_1, v_2 = (sol[i], sol[j]) if sol[i] < sol[j] else (
              sol[j], sol[i])  # v_1 < v_2 make indexing in tb_list and fq_dict convenient
          delta = get_delta(no_v, adj_mat, sol, i, j)
          if (v_1, v_2) not in tb_list:  # if not tabu
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
        
          new_sol = get_new_sol(sol, best_i_0, best_j_0)
          new_cost = cost + best_delta_0
      # assert abs(new_cost - get_cost(n, adj_mat, new_sol)) < 1e-9, 'new_sol does not match new_cost'
      return new_sol, new_cost, tb_list

