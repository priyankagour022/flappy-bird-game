import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 600
FPS = 60
GRAVITY = 0.25
FLAP_FORCE = -5
PIPE_VELOCITY = -4
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
bird_img = pygame.image.load("/home/priyanka/Documents/flappy-bird-game/images/bird.jpg").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (30, 30))  # Resize the bird image
pipe_img = pygame.image.load("/home/priyanka/Documents/flappy-bird-game/images/pipe.png").convert_alpha()
cloud_img = pygame.image.load("/home/priyanka/Documents/flappy-bird-game/images/background.png").convert_alpha()
cloud_img = pygame.transform.scale(cloud_img, (WIDTH, HEIGHT))  # Resize the cloud image to fit the screen

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = GRAVITY
        self.image = bird_img
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def flap(self):
        self.velocity = FLAP_FORCE

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.image = pipe_img
        self.top_rect = self.image.get_rect(topleft=(self.x, 0))
        self.bottom_rect = self.image.get_rect(topleft=(self.x, self.height + PIPE_GAP))

    def update(self):
        self.x += PIPE_VELOCITY
        self.top_rect.topleft = (self.x, 0)
        self.bottom_rect.topleft = (self.x, self.height + PIPE_GAP)

    def offscreen(self):
        return self.x < -100

# Functions
def draw_window():
    screen.fill(WHITE)
    screen.blit(cloud_img, (0, 0))  # Draw the cloud image as the background
    for pipe in pipes:
        screen.blit(pipe.image, pipe.top_rect)
        screen.blit(pipe.image, pipe.bottom_rect)
    screen.blit(bird.image, bird.rect)
    pygame.display.update()

# Rest of the code remains unchanged...


def check_collision():
    if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    return False

def restart_game():
    global bird, pipes, score
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    score = 0

# Initialize game objects
bird = Bird()
pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
score = 0

# Main game loop
running = True
game_over = False
while running:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()

        bird.update()

        if bird.rect.colliderect(pipes[0].top_rect) or bird.rect.colliderect(pipes[0].bottom_rect):
            game_over = True

        if pipes[0].offscreen():
            pipes.pop(0)
            pipes.append(Pipe(WIDTH))
            score += 1

        for pipe in pipes:
            pipe.update()

        if check_collision():
            game_over = True

        draw_window()
        clock.tick(FPS)

    # Game Over screen
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render("Score: " + str(score), True, BLACK)
    restart_text = font.render("Restart", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # Draw game over screen with restart button
    screen.fill(WHITE)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)

    # Draw restart button with green background
    restart_button = pygame.Surface((restart_rect.width + 20, restart_rect.height + 10))
    restart_button.fill(GREEN)
    restart_button_rect = restart_button.get_rect(center=restart_rect.center)
    screen.blit(restart_button, restart_button_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(mouse_pos):
                restart_game()
                game_over = False

pygame.quit()
sys.exit()