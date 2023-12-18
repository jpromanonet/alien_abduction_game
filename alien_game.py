import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)  # Orange color for the score rectangle
STAR_COUNT = int(WIDTH * HEIGHT * 0.001)  # Adjust star count

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Abduction Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player (alien spaceship)
player_rect = pygame.Rect(WIDTH // 2 - 25, 10, 50, 50)
player_speed = 5

# List to store targets (animals)
targets = []

# Set initial score
score = 0

# Font for displaying the score
font = pygame.font.Font(None, 36)

# Flag to track if spacebar is pressed
space_pressed = False

# Counter to control the pace of target appearances
target_spawn_counter = 0
TARGET_SPAWN_RATE = 120  # Adjust the rate to control the pace (higher values make it slower)

# List to store stars
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3)} for _ in range(STAR_COUNT)]

# Grassy area at the bottom
grass_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            space_pressed = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_pressed = False

    keys = pygame.key.get_pressed()

    # Move the player
    player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

    # Ensure the player stays within the screen boundaries
    player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

    # Spawn a new target based on the counter
    target_spawn_counter += 1
    if target_spawn_counter >= TARGET_SPAWN_RATE:
        target_rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT - 20, 20, 20)
        targets.append(target_rect)
        target_spawn_counter = 0

    # Update star glow animation
    for star in stars:
        star['size'] += 0.05
        if star['size'] > 3:
            star['size'] = 1

    # Clear the screen
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star['x'], star['y']), int(star['size']))

    # Draw the grassy area
    pygame.draw.rect(screen, GREEN, grass_rect)

    # Draw the player and targets
    pygame.draw.rect(screen, GREEN, player_rect)
    for target in targets:
        pygame.draw.rect(screen, WHITE, target)

    # Draw the tractor beam when spacebar is pressed
    if space_pressed:
        tractor_beam_rect = pygame.Rect(player_rect.centerx - 2, player_rect.centery, 4, HEIGHT - player_rect.centery)
        pygame.draw.line(screen, GREEN, (player_rect.centerx, player_rect.centery),
                         (player_rect.centerx, HEIGHT), 2)

        # Check for collisions with targets
        for target in targets[:]:
            if tractor_beam_rect.colliderect(target):
                # Change the color of the tractor beam to green
                pygame.draw.line(screen, GREEN, (player_rect.centerx, player_rect.centery),
                                 (player_rect.centerx, target.bottom), 2)
                # Change the color of the target to red
                pygame.draw.rect(screen, RED, target)
                targets.remove(target)
                score += 1

    # Draw the score in an orange rectangle
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()