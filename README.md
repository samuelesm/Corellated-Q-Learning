# Corellated-Q-Learning

In this project, four different Q-Learning Algorithms are compared

# Abstract

In 2003, Amy Greenwald and Keith Hall published a paper titled “Correlated Q-Learning”. In their 
report, they experimented with four different Q algorithms, Correlated-Q, Foe-Q, Friend-Q, and 
classic Q-Learning, and graphed the convergence of the Q-value difference between the updated 
Q of the starting state and the previous one. Once the difference in the algorithms’ graphs
converges to a difference of 0, we know that convergence is completed. The purpose of this report 
is to replicate the graph results of Figure 3 in the paper to confirm their findings, and show that 
Correlated-Q and Foe-Q yield similar graphs and that classical Q-Learning is the least efficient 
among the algorithms and fails to converge even after a million iterations. The Correlated-Q 
algorithm is based off the Nash-Q algorithm in the Hu and Wellman 1998 paper, but the Nash 
equilibrium was too cumbersome to calculate. As a result, correlated equilibriums (CE) was 
introduced as a solution that uses linear programing to enable a more digestible way of computing
it similarly. Lastly, the Friend-Q and Foe-Q algorithms are derived from the Littman 2001 paper. 
Through clever implementation of multiplayer MDP with multi-agent Q-Learning, classical QLearning can be greatly outperformed. 

## Q Update Eqution



## Four Algorithms and Results
All four algorithms used the same Q update equation shown above with just the Vi(s) 
portion being changed out for each algorithm.

1) Correlated-Q used a glpk solver from the cvxopt library to linearly solve the expected returns of 
player A and player B by generating a correlation matrix, generating b and c vectors, and 
inputting it into a solver. 

2) Foe-Q was similar in that it used a glpk solver to linearly solve expected outcomes for its Q 
table. However, it only had one Q-table instead of two. Also, its A matrix was its current Q 
values with a column of ones attached at the end instead of a correlation matrix. 

3) Friend-Q didn’t use any solvers. It instead took the maximum value from the Q-table, and its Qtable was for both players. No epsilon was used. 
Q-Learning used a classical approach with greedy decaying epsilon. It is almost identical to 

4) Friend-Q here, but instead of having a Q-table for both players, it was only for player A.
