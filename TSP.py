class TSP:


    def cost( n, adjacency_matrix , solution):
     return sum([adjacency_matrix[  solution[_]  ][  solution[(_ + 1) % n]  ] for _ in range(n)])
    
    def swap_Solution(solution , i , j):
     new_solution= solution.copy()
     new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
     return new_solution

    def twoOpt_Solution(solution , i , j):
     new_solution = sol.copy()
     new_solution[i:j+1] = new_solution[i:j+1][::-1]  
     return new_solution

    def delta_Swap(n, adjacency_matrix , solution , i , j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[j]][solution[(i + 1) % n]] + \
             adjacency_matrix[solution[j - 1]][solution[i]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[i]][solution[(i + 1) % n]] - \
             adjacency_matrix[solution[j - 1]][solution[j]] - adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if j - i == 1 or i == 0 and j == n - 1:
        delta += 2 * adjacency_matrix[sol[i]][sol[j]]  # symmetrical TSP
     return delta

    
    def delta_twoOpt(n, adjacency_matrix , solution , i , j):
     delta = adjacency_matrix[solution[i - 1]][solution[j]] + adjacency_matrix[solution[i]][solution[(j + 1) % n]] - \
             adjacency_matrix[solution[i - 1]][solution[i]] - adjacency_matrix[solution[j]][solution[(j + 1) % n]]
     if i == 0 and j == n - 1:  # the first two value == 0, while others < 0
        delta = 0
     return delta
     

