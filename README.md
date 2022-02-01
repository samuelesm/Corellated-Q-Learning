# Corellated-Q-Learning

In this project, four different Q-Learning Algorithms are compared

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/map.png">
</p>

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

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/Q-Equation.png">
</p>

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

### Results

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/corr-q.png" width="800">
</p>

In figure A, we see the simulated Q-value difference error for the simulated and the 
original graphs respectively. Remarkably, the trend of both graphs seems to be following the
same trend up until a little bit past the 400 thousandth mark. Afterwards, the Q-value difference 
seems to be going back a bit upwards, whereas it has a continuous downwards trend in the 
original. This may be attributed to different alpha and gamma parameter tweaking. Another
theory is that in the simulation, there may be some noise the is introduce in the correlation matrix 
that gets mixed in. We can see the proof of this in the appendix for another run of the algorithm.

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/foe-q.png" width="800">
</p>

Next, we see the simulated and original graphs for Foe-Q. We can see that the graphs a very 
similar. Although we didn’t get the results we wanted for the simulated Correlation-Q graph and 
Foe-Q also used the same solver, the simpler approach in creating the system of equations may 
have attributed to it coming out cleaner.

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/friend-q.png" width="800">
</p>

The both graphs for Friend-Q converged very quickly. A theory behind its quick convergence is
its multi-agent approach allows for one table to gather data and correct itself relatively quickly. 
Also, it doesn’t get its expected values from a system of equations, but rather from gathering the 
best values. Always choosing the best value is what likely led it to its fast convergence.

<p align="center">
<img src="https://github.com/samuelesm/Corellated-Q-Learning/blob/main/q-learn.png" width="800">
</p>

The original graph for Q-Learning is very convoluted. If it is not because of noise, we can see 
two downwards trends that alternate between each other. The simulated graph more closely 
resembles the graph that is part of the lower trend. The simulated Q-learning converges the 
slowest, but it is consistently on a downward trend. Although more similar to Friend-Q, which 
converged the fastest, its slower or non-converging trend can be attributed to it only considering 
one player as its agent, limiting cross-correlated data. As a result, Greenwald and Hall were able 
to show the advantage of multi-agent Q-Learning and its benefits of speed in comparison to 
traditional Q-Learning.
