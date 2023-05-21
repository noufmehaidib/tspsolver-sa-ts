# Overview
This application solves Traveling SalesMan Problem (TSP) using two meta-heuristic Simulated Annealing (SA) and Tabu Search (TS).
Term project of Selected Topics in Computer Science, King Saud Universty Course.

# Details of implementation 
The tsp solver has 4 classes: 


         -----------> MAIN.py:
                      where the program starts.
         -----------> SA.py:
                      detailed implementation of the SA algorithm
         -----------> TS.py:
                      detailed implementation of the TS algorithm.
         -----------> TSP.py:
                      detailed implementation of the TSP.

The tsp solver has 2 folders:

        -----------> data:
                     contains the test bed used.
        -----------> results:
                     displays the figure of the convergence.
                     
 # Getting Started
 Test bed `dj38.txt` and `qa194.txt` can be found in [National Travelling Salesman Problem](http://www.math.uwaterloo.ca/tsp/world/countries.html#DJ).
 The optimal tour length is obtained from the same site, and then the value obtained is used as `opt_cost` in `main.py` to calculate the optimality gap.

 To run the program, open `main.py` and choose your prefered algorithm/neighborhood structure.
