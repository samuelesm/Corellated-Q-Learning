import numpy as np
import matplotlib.pyplot as plt
import soccer_game
from cvxopt import matrix, solvers


def FoeQ(game, playerA, playerB):
    alpha = 1.0
    alpha_min = 0.001
    alpha_decay = (alpha - alpha_min) / 1000000
    gamma = 0.9
    # Initializing Q-tables for each player with the dimensionality being represented by: 
    # [S: player A position, S: player B position, S: ball posession, A: player A action, A: player B action]
    Q_table = np.zeros([8, 8, 2, 5, 5])

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

        Q_hist = Q_table[2, 1, 1, 2, 4]
        playerA_position = playerA.position
        playerB_position = playerB.position
        game_ball = game.ball_possession

        # Generate random player actions and the order of player actions
        pA_action = np.random.randint(5)
        pB_action = np.random.randint(5)
        p_order = np.random.randint(2)

        # Play one step in the game
        pA_rew, pB_rew, pA_pos, pB_pos, ball_poss, done = game.play_game(playerA, playerB, pA_action, pB_action, p_order)

        # Solve for expected Q for current state: get current Q for state
        # Q_T = np.array(Q_table[playerA_position, playerB_position, game_ball])
        Q_T = matrix(Q_table[playerA_position, playerB_position, game_ball]).trans()
        n = Q_T.size[1]

        # Make A matrix and b and c vectors
        A = np.hstack((np.ones((Q_T.size[0], 1)), Q_T))
        ID_mat = np.hstack((np.zeros((n, 1)), -(np.identity(n))))
        A = np.vstack((A, ID_mat))
        A = matrix(np.vstack((A, np.hstack((0, np.ones(n))), np.hstack((0, -(np.ones(n)))))))
        b = matrix(np.hstack((np.zeros(A.size[0] - 2), [1, -1])))
        c = matrix(np.hstack(([-1], np.zeros(n))))
        # Use glpk solver
        solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}
        solution = solvers.lp(c, A, b, solver = 'glpk')
        update = solution['primal objective']
        if update is None:
            update = 0

        # Update Q-table
        Q_table[playerA_position, playerB_position, game_ball, pA_action, pB_action] = (1 - alpha) * Q_table[playerA_position, playerB_position, game_ball, pA_action, pB_action] + alpha * ((1 - gamma) * pA_rew + gamma * update)
        # Store data for graph whenever game is reset
        if [playerA_position, playerB_position, game_ball, pA_action, pB_action] == [2, 1, 1, 2, 4]:
            Q_val_diff.append(abs(Q_table[2, 1, 1, 2, 4] - Q_hist))
            iteration_num.append(iteration)
            # print(iteration, abs(Q_table[2, 1, 1, 2, 4] - Q_hist))
        # Decrement alpha
        alpha = alpha - alpha_decay

    return Q_val_diff, iteration_num

playerA = soccer_game.Player("A", 0)
playerB = soccer_game.Player("B", 1)
game = soccer_game.SoccerArena(playerA, playerB)

Q_diffs, iteration = FoeQ(game, playerA, playerB)

plt.plot(iteration, Q_diffs)
plt.title("Foe-Q")
plt.xlabel("Simulation Iteration")
plt.ylabel("Q-Value Difference")
plt.show()