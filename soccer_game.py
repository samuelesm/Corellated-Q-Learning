import numpy as np

class Player():
    def __init__(self, name, team_num):
        self.name = name
        self.points = 0
        self.position = 0
        self.team_num = team_num


class SoccerArena():
    def __init__(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB
        self.start_spaceA = [2, 6]  # Starting spots
        self.start_spaceB = [1, 5]
        self.goal_spaceA = [0, 4]  # Goal spots
        self.goal_spaceB = [3, 7]

        self.ball_possession = 1
        self.ball_position = playerB.position

    def start(self):
        # Start player A and B on random spots on the side opposite to their goals
        center_space = [1, 2, 5, 6]
        rand_arr = np.random.choice(len(center_space), 2, replace=False)
        self.playerA.pos = center_space[rand_arr[0]]
        self.playerB.pos = center_space[rand_arr[1]]

        self.ball_possession = np.random.randint(2)
        if self.ball_possession == 0:
            self.ball_position = self.playerA.position
            self.ball_possession = self.playerA.team_num
        else:
            self.ball_position = self.playerB.position
            self.ball_possession = self.playerB.team_num

    def move_intent(self, player, action):
        in_A_goal = player.position in self.goal_spaceA
        in_B_goal = player.position in self.goal_spaceB
        if action == 1 and not in_B_goal:  # Go East
            return player.position + 1
        elif action == 3 and not in_A_goal:  # Go West
            return player.position - 1
        elif action == 2 and player.position >= 4:  # Go South
            return player.position - 4
        elif action == 0 and player.position <= 3:  # Go North
            return player.position + 4
        else:  # Stick to current position
            return player.position

    def play_game(self, pA, pB, pA_action, pB_action, order):
        # Check whether player A or B is moving first and assign variables accordingly
        if order == 0:
            p1 = pA
            p2 = pB
            p1_action = pA_action
            p2_action = pB_action
        else:
            p1 = pB
            p2 = pA
            p1_action = pB_action
            p2_action = pA_action

        # Get intended action coordinate
        move_intent_p1 = self.move_intent(p1, p1_action)
        move_intent_p2 = self.move_intent(p2, p2_action)
        # Check if player1 is intending to move into where player 2 is, switch possession if true
        if move_intent_p1 != p2.position:
            p1.position = move_intent_p1
        else:
            self.ball_possession = p2.team_num
        # Check if player2 is intending to move into where player 1 is, switch possession if true
        if move_intent_p2 != p1.position:
            p2.position = move_intent_p2
        else:
            self.ball_possession = p1.team_num

        # move ball with whomever possesses it
        if self.ball_possession == 0:
            self.ball_position = self.playerA.position
        else:
            self.ball_position = self.playerB.position


        ## Check position of ball to determine the end of a round and allocate rewards
        if self.ball_position in self.goal_spaceA:
            pA_reward = 100
            pB_reward = -100
            done = True
        elif self.ball_position in self.goal_spaceB:
            pA_reward = -100
            pB_reward = 100
            done = True
        else:
            pA_reward = 0
            pB_reward = 0
            done = False

        return pA_reward, pB_reward, self.playerA.position, self.playerB.position, self.ball_possession, done