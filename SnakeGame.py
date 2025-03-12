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
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.snake = [self.head, [self.head[0] - BLOCK_SIZE, self.head[1]], [self.head[0] - (2 * BLOCK_SIZE), self.head[1]]]
        self.score = 0
        self.food = self.create_food()
        self.iteration = 0
    
    def play_step(self, action):
        self.iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        reward = 0
        game_over = False

        self.move(action)   
        self.snake.insert(0, self.head)

        if self.food in self.snake:
            reward = 100
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()
        
        if self.collision():
            reward = -100
            game_over = True
        
        return reward, game_over, self.score

    def create_food(self):
        return [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
    
    def move(self, action):
        pass

    def collision(self):
        pass
