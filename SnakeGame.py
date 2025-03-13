import pygame
import random

HEIGHT = 600
WIDTH = 800
BLOCK_SIZE = 20
SPEED = 100
DIRECTIONS = ["RIGHT", "DOWN", "LEFT", "UP"]

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        self.direction = 0
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

        if self.head == self.food:
            reward = 100
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()
        
        if self.is_collision(self.head) or self.iteration > 100 * len(self.snake):
            reward = -100
            game_over = True
        
        self.update_display()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def create_food(self):
        return [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
    
    def move(self, action):
        if (action[0]):       # Straight
            pass
        elif (action[1]):     # Move right
            self.direction = (self.direction + 1) % 4
        else:                   # Move left
            self.direction = (self.direction - 1) % 4

        new_head = self.head[:]
        if (self.direction == 0):
            new_head[0] += BLOCK_SIZE
        elif (self.direction == 1):
            new_head[1] += BLOCK_SIZE
        elif (self.direction == 2):
            new_head[0] -= BLOCK_SIZE
        else:
            new_head[1] -= BLOCK_SIZE            

        self.snake.insert(0, new_head)
        self.head = new_head

    def is_collision(self, point):
        if point[0] >= WIDTH or point[0] < 0 or point[1] >= HEIGHT or point[1] < 0:
            return True
        if point in self.snake[1:]:
            return True
        return False
    
    def update_display(self):
        self.display.fill((0, 0, 0))
        for block in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        self.display.blit(pygame.font.SysFont('Arial', 20).render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        pygame.display.flip()
        self.clock.tick(10)