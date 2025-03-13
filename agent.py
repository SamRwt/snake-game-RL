import torch
import random
import numpy as np

from SnakeGame import SnakeGame, BLOCK_SIZE, DIRECTIONS

MAX_MEMORY = 100000
ACTIONS = ["STRAIGHT", "RIGHT", "LEFT"]

class Agent:
    def __init__(self):
        self.count_games = 0
        self.epsilon = 0    # Randomness
        self.memory = []
        self.model = None
        self.trainer = None

    def _will_collide(self, game, game_dir, action_dir):
        move_dir = 0
        if (action_dir == 0):
            move_dir = game_dir
        elif (action_dir == 1):
            move_dir = (game_dir + 1) % 4
        else:
            move_dir = (game_dir - 1) % 4
        
        
        head = game.snake[0].copy()
        if move_dir == 0:
            head[0] += BLOCK_SIZE
        elif move_dir == 1:
            head[1] += BLOCK_SIZE
        elif move_dir == 2:
            head[0] -= BLOCK_SIZE
        else:
            head[1] -= BLOCK_SIZE
        
        return game.is_collision(head)
    
            
    def get_state(self, game):
        head = game.snake[0]
        game_dir = game.direction
        state_collision = [
            self._will_collide(game, game_dir, 0), # Move straight
            self._will_collide(game, game_dir, 1), # Move right
            self._will_collide(game, game_dir, 2)  # Move left
        ]
        state_direction = [
            game_dir == 0, # Going right
            game_dir == 1, # Going down
            game_dir == 2, # Going left
            game_dir == 3  # Going up
        ]
        state_food = [
            game.food[0] < head[0],
            game.food[0] > head[0],
            game.food[1] < head[1],
            game.food[1] > head[1] 
        ]

        return np.array(state_collision + state_direction + state_food)

    def get_action(self, state):
        self.epsilon = 100 * np.exp(-0.01 * self.count_games)
        my_action = [0, 0, 0]
        if random.random() < self.epsilon:
            action = random.randint(0, 2)
            my_action[action] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            action = torch.argmax(prediction).item()
            my_action[action] = 1
        
        return my_action


if __name__ == "__main__":
    agent = Agent()
    game = SnakeGame()
    
    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)

        reward, game_over, score = game.play_step(action)
        
        state_new = agent.get_state(game)
        agent.trainer.train_step(state_old, action, reward, state_new, game_over)

        agent.memory.append((state_old, action, reward, state_new, game_over))
        if len(agent.memory) > MAX_MEMORY:
            agent.memory.pop(0)
        
        if game_over:
            game.reset()
            agent.count_games += 1
            print(f"Game {agent.count_games} Score: {score}")