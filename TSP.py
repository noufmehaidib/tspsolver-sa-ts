class TSP:


    def cost( n, adjacency_matrix , solution):
     return sum([adjacency_matrix[  solution[_]  ][  solution[(_ + 1) % n]  ] for _ in range(n)])

    def swap_Solution(solution , i , j):
     new_solution= solution.copy()
     new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
     return new_solution

    def twoOpt_Solution(solution , i , j):
      new_solution = solution.copy()
      new_solution[i:j+1] = new_solution[i:j+1][::-1]
      return new_solution

    def delta_Swap(n, adjacency_matrix , solution , i , j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[j]][solution[(i + 1) % n]] + \
             adjacency_matrix[solution[j - 1]][solution[i]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[i]][solution[(i + 1) % n]] - \
             adjacency_matrix[solution[j - 1]][solution[j]] - adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if j - i == 1 or i == 0 and j == n - 1:
        delta += 2 * adjacency_matrix[solution[i]][solution[j]]  # symmetrical TSP
     return delta


    def delta_twoOpt(n, adjacency_matrix , solution , i , j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if i == 0 and j == n - 1:  # the first two value == 0, while others < 0
        delta = 0
     return delta

    def tnm_selection(n, adj_mat, current_sol, max_tnm, ngh_strc, tb_size, tb_list, fq_dict, best_cost,tabu_tenure):
      """
      : n: number of vertices
      : adj_mat: adjacency matrix
      : sol: solution where the neighbours are chosen from
      : max_tnm: how many candidates picked in tournament selection
      : ngh_strc: [get_sol, get delta], method of mutation, e.g. swap, 2-opt
      : tb_size: >=0, max length of tb_list
      : tb_list: deque ,out <- [...] <- in
      : fq_dict: visit times of a solution in the tabu list
      : tabu_tenure: max number of iteration that a solution stays in the tabu list
      : best_cost: cost of the best solution
      """

      get_new_sol = ngh_strc[0]
      get_delta = ngh_strc[1]

      cost_current_sol = TSP.cost(n, adj_mat, current_sol)

      best_delta_0 = math.inf
      best_i_0 = best_j_0 = -1 # To determine the best move

      best_delta_1 = math.inf
      best_i_1 = best_j_1 = -1

      for l in range(max_tnm):

          for key in fq_dict.keys(): fq_dict[(key)] = fq_dict.get(key,0) + 1 # update the number of iteration that the solution stays in the tabu list
          i, j = random.sample(range(n), 2)  # randomly select two indexes
          i, j = (i, j) if i < j else (j, i)  # let i < j

          sol_to_test=get_new_sol(current_sol, i, j)
          delta = get_delta(n, adj_mat, current_sol, i, j)
          if tuple(sol_to_test) not in tb_list:  # if the sol is not tabu
              if delta < best_delta_0:
                  best_delta_0 = delta
                  best_i_0 = i
                  best_j_0 = j
          else:  # If it in tabu it will be accepted if it has an improvement over the current best solution to escape from local optima
              if delta < best_delta_1:
                  best_delta_1 = delta
                  best_i_1 = i
                  best_j_1 = j
      if best_delta_1 < best_delta_0 and cost_current_sol + best_delta_1 < best_cost:  # break the tabu
          new_sol = get_new_sol(current_sol, best_i_1, best_j_1)
          new_cost = cost_current_sol + best_delta_1
          k = new_sol
          tb_list.remove(tuple(k))
          tb_list.append(tuple(k))  # move to the end of list
          fq_dict[tuple(k)] += 1 # update fq_dict
      else:  # do not break the tabu
          if tb_size > 0:
              if len(tb_list) == tb_size:
                  k = tb_list.popleft()
                  if k in fq_dict.keys():
                    fq_dict.pop(tuple(k))
              new_sol = get_new_sol(current_sol, best_i_0, best_j_0)
              new_cost = cost_current_sol + best_delta_0
              k = new_sol
              fq_dict[tuple(k)] =  1 # update fq_dict
              tb_list.append(tuple(k))
      keys=[]
      for key , v in fq_dict.items() :
        if v >= tabu_tenure :
          keys.append(key)
      for key in keys :  # a solution in the tabu list removed if exceed tabu_tenure
        fq_dict.pop(key)
        tb_list.remove(key)

      return new_sol, new_cost, tb_list, fq_dict
