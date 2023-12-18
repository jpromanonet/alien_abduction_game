import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color for the level indicator
SHIP_GREEN = (0, 255, 0)  # Green color for the ship
GRASS_GREEN = (0, 100, 0)  # Darker green color for the grass
STAR_COUNT = int(WIDTH * HEIGHT * 0.001)

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

# Font for displaying the score, level, and timer
font = pygame.font.Font(None, 36)

# Flag to track if spacebar is pressed
space_pressed = False

# Counter to control the pace of target appearances
target_spawn_counter = 0
TARGET_SPAWN_RATE = 120  # Adjust the rate to control the pace (higher values make it slower)

# List to store stars
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3),
          'color': LIGHT_BLUE} for _ in range(STAR_COUNT)]

# Grassy area at the bottom
grass_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)

# Level and Countdown Variables
current_level = 1
abduction_target = 10  # Initial target
countdown_timer = 60  # Initial countdown timer in seconds

# List of colors for each level
level_colors = [
    LIGHT_BLUE,
    ORANGE,
    RED,
    YELLOW,
    GRAY,
    (0, 255, 0),  # Green
    (255, 0, 255),  # Purple
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Indigo
]

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

    # Update star glow animation and color for the current level
    for star in stars:
        star['size'] += 0.05
        if star['size'] > 3:
            star['size'] = 1
        star['color'] = level_colors[current_level - 1]

    # Clear the screen
    screen.fill(BLACK)

    # Draw stars with level-based color
    for star in stars:
        pygame.draw.circle(screen, star['color'], (star['x'], star['y']), int(star['size']))

    # Draw the grassy area
    pygame.draw.rect(screen, GRASS_GREEN, grass_rect)

    # Draw the player and targets
    pygame.draw.rect(screen, SHIP_GREEN, player_rect)
    for target in targets:
        pygame.draw.rect(screen, WHITE, target)

    # Draw the tractor beam when spacebar is pressed
    if space_pressed:
        tractor_beam_rect = pygame.Rect(player_rect.centerx - 2, player_rect.centery, 4, HEIGHT - player_rect.centery)
        pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                         (player_rect.centerx, HEIGHT), 2)

        # Check for collisions with targets
        for target in targets[:]:
            if tractor_beam_rect.colliderect(target):
                # Change the color of the tractor beam to yellow
                pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                                 (player_rect.centerx, target.bottom), 2)
                # Change the color of the target to red
                pygame.draw.rect(screen, RED, target)
                targets.remove(target)
                score += 1

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top center
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(center=(WIDTH // 2, 20))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the countdown timer in a red rectangle at the top right
    timer_text = font.render(f"Time: {int(countdown_timer)}", True, WHITE)
    timer_rect = timer_text.get_rect(topright=(WIDTH - 10, 10))
    pygame.draw.rect(screen, RED, timer_rect.inflate(10, 5))
    screen.blit(timer_text, timer_rect)

    # Draw the targets to acquire for the current level in a gray rectangle at the top right
    targets_text = font.render(f"Abductions: {score}/{abduction_target}", True, WHITE)
    targets_rect = targets_text.get_rect(topright=(WIDTH - 10, 60))
    pygame.draw.rect(screen, GRAY, targets_rect.inflate(10, 5))
    screen.blit(targets_text, targets_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

   # Countdown Timer Logic
    countdown_timer -= 1 / FPS  # Decrease the timer based on the frame rate
    if countdown_timer <= 0:
        print(f"Level {current_level} completed! Score: {score}")
        current_level += 1
        score = 0  # Reset the score for the next level
        abduction_target += 10  # Increase the target for the next level
        countdown_timer = 60  # Reset the countdown timer for the next level

    # Check if the player reached the abduction target for the current level
    if score >= abduction_target:
        # Move to the next level
        current_level += 1
        abduction_target += 10  # Increase the target for the next level
        countdown_timer = 60  # Reset the countdown timer for the next level
 
# Quit Pygame
pygame.quit()