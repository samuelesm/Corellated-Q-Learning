import numpy as np
import matplotlib.pyplot as plt
import soccer_game
from cvxopt import matrix, solvers


def QLearning(game, playerA, playerB):
    alpha = 0.9
    alpha_min = 0.001
    epsilon = 0.9
    epsilon_min = 0.001
    alpha_decay = (alpha - alpha_min) / 1000000
    epsilon_decay = (epsilon - epsilon_min) / 1000000
    gamma = 0.9
    
    # Initializing Q-tables for each player with the dimensionality being represented by: 
    # [S: player A position, S: player B position, S: ball posession, A: player A action, A: player B action]
    Q_table = np.zeros([8, 8, 2, 5])

    Q_val_diff = []
    iteration_num = []
    game.start()
    done = False

    # Iterate 1 million game moves
    for iteration in range(1000000):
        # Start new game if ball reaches a goal
        if done == True:
            game.start()
            done = False

        Q_hist = Q_table[2, 1, 1, 2]
        playerA_position = playerA.position
        playerB_position = playerB.position
        game_ball = game.ball_possession

        # Generate random player actions with Greedy Epsilon Selection
        if epsilon > np.random.random():
            pA_action = np.random.randint(5)
        else:
            pA_action = np.argmax(Q_table[playerA_position, playerB_position, game_ball])
        pB_action = np.random.randint(5)
        p_order = np.random.randint(2)

        # Play one step in the game
        pA_rew, pB_rew, pA_pos, pB_pos, ball_poss, done = game.play_game(playerA, playerB, pA_action, pB_action, p_order)

        # Update Q-table
        Q_table[playerA_position, playerB_position, game_ball, pA_action] = \
        (1 - alpha) * Q_table[playerA_position, playerB_position, game_ball, pA_action] + \
        alpha * ((1 - gamma) * pA_rew + gamma * np.max(Q_table[pA_pos, pB_pos, ball_poss]))

        # Store data for graph whenever game is reset
        if [playerA_position, playerB_position, game_ball, pA_action] == [2, 1, 1, 2]:
            Q_val_diff.append(abs(Q_table[2, 1, 1, 2] - Q_hist))
            iteration_num.append(iteration)
            # print(iteration, abs(Q_table[2, 1, 1, 2] - Q_hist))
        # Decrement alpha
        alpha = alpha - alpha_decay

    return Q_val_diff, iteration_num

playerA = soccer_game.Player("A", 0)
playerB = soccer_game.Player("B", 1)
game = soccer_game.SoccerArena(playerA, playerB)

Q_diffs, iteration = QLearning(game, playerA, playerB)

plt.plot(iteration, Q_diffs)
plt.title("Q-Learning")
plt.xlabel("Simulation Iteration")
plt.ylabel("Q-Value Difference")
plt.show()