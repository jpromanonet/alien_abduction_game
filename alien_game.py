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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Shoot tractor beam when spacebar is pressed
            tractor_beam_rect = pygame.Rect(player_rect.centerx - 2, player_rect.centery, 4, HEIGHT - player_rect.centery)
            for target in targets[:]:
                if tractor_beam_rect.colliderect(target):
                    # Change the color of the target to red
                    pygame.draw.rect(screen, RED, target)
                    targets.remove(target)
                    score += 1

    keys = pygame.key.get_pressed()

    # Move the player
    player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

    # Ensure the player stays within the screen boundaries
    player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

    # Spawn a new target
    if random.randint(1, 100) < 3:  # Adjust the frequency of target spawns
        target_rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT - 20, 20, 20)
        targets.append(target_rect)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player and targets
    pygame.draw.rect(screen, GREEN, player_rect)
    for target in targets:
        pygame.draw.rect(screen, WHITE, target)

    # Draw the tractor beam
    pygame.draw.line(screen, WHITE, (player_rect.centerx, player_rect.centery),
                     (player_rect.centerx, HEIGHT), 2)

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
