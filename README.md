# Corellated-Q-Learning

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
