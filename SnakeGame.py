import pygame, random

HEIGHT = 600
WIDTH = 800
BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        self.direction = 'RIGHT'
        self.snake = [[WIDTH // 2, HEIGHT // 2]]    # start at the center
        self.food = self.create_food()
    
    def create_food(self):
        return [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]

    # TODO: Step (L, R, U, D), collision detection (wall, self, food), game over