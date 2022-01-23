import numpy as np
import matplotlib.pyplot as plt
import soccer_game
from cvxopt import matrix, solvers


def uCEQ(game, playerA, playerB):
    alpha = 0.9
    alpha_min = 0.001
    alpha_decay = (alpha - alpha_min) / 1000000
    gamma = 0.9
    # Initializing Q-tables for each player with the dimensionality being represented by: 
    # [S: player A position, S: player B position, S: ball posession, A: player A action, A: player B action]
    Q_playerA = np.zeros([8, 8, 2, 5, 5])
    Q_playerB = np.zeros([8, 8, 2, 5, 5])

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

        Q_hist = Q_playerA[2, 1, 1, 2, 4]
        playerA_position = playerA.position
        playerB_position = playerB.position
        game_ball = game.ball_possession

        # Generate random player actions and the order of player actions
        pA_action = np.random.randint(5)
        pB_action = np.random.randint(5)
        p_order = np.random.randint(2)

        # Play one step in the game
        pA_rew, pB_rew, pA_pos, pB_pos, ball_poss, done = game.play_game(playerA, playerB, pA_action, pB_action, p_order)

        # Solve for expected Q        
        action_mat = matrix(Q_playerA[playerA_position, playerB_position, game_ball]).trans()
        n = action_mat.size[1]
        A = np.zeros((2 * n * (n - 1), n * n))
        Q_A = np.array(Q_playerA[playerA_position, playerB_position, game_ball])
        Q_B = np.array(Q_playerB[playerA_position, playerB_position, game_ball])

        cnt = 0
        for i in range(n):
            for j in range(n):
                if i != j:
                    A[cnt, i * n:(i + 1) * n] = Q_A[i] - Q_A[j]
                    A[cnt + n * (n - 1), i:(n * n):n] = Q_B[:, i] - Q_B[:, j]
                    cnt += 1
        # Generate Correlation Matrix, Make A matrix and b and c vectors
        A = matrix(A)
        A = np.hstack((np.ones((A.size[0], 1)), A))
        A = np.vstack((A, np.hstack((np.zeros((n*n, 1)), -np.identity(n*n)))))
        A = matrix(np.vstack((A, np.hstack((0,np.ones(n*n))), np.hstack((0,-np.ones(n*n))))))
        b = matrix(np.hstack((np.zeros(A.size[0] - 2), [1, -1])))
        c = matrix(np.hstack(([-1.], -(Q_A + Q_B).flatten())))
        # Use glpk solver
        solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}
        solution = solvers.lp(c, A, b, solver = 'glpk')
        if solution['x'] is None:
            QA_exp_return = 0
            QB_exp_return = 0
        # Get expected return
        else: 
            distance = solution['x'][1:]
            Q_A_vec = Q_A.flatten()
            Q_B_vec = Q_B.transpose().flatten()
            QA_exp_return = np.matmul(Q_A_vec, distance)[0]
            QB_exp_return = np.matmul(Q_B_vec, distance)[0]

        # Update Q-table
        Q_playerA[playerA_position, playerB_position, game_ball, pA_action, pB_action] = (1 - alpha) * Q_playerA[playerA_position, playerB_position, game_ball, pA_action, pB_action] + alpha * ((1 - gamma) * pA_rew + gamma * QA_exp_return)
        Q_playerB[playerA_position, playerB_position, game_ball, pA_action, pB_action] = (1 - alpha) * Q_playerB[playerA_position, playerB_position, game_ball, pA_action, pB_action] + alpha * ((1 - gamma) * pB_rew + gamma * QB_exp_return)
        # Store data for graph whenever game is reset
        if [playerA_position, playerB_position, game_ball, pA_action, pB_action] == [2, 1, 1, 2, 4]:
            Q_val_diff.append(abs(Q_playerA[2, 1, 1, 2, 4] - Q_hist))
            iteration_num.append(iteration)
            # print(iteration, abs(Q_playerA[2, 1, 1, 2, 4] - Q_hist))
        # Decrement alpha
        alpha = alpha - alpha_decay

    return Q_val_diff, iteration_num

playerA = soccer_game.Player("A", 0)
playerB = soccer_game.Player("B", 1)
game = soccer_game.SoccerArena(playerA, playerB)

Q_diffs, iteration = uCEQ(game, playerA, playerB)

plt.plot(iteration, Q_diffs)
plt.title("uCE-Q")
plt.xlabel("Simulation Iteration")
plt.ylabel("Q-Value Difference")
plt.show()