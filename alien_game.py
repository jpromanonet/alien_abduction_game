import pygame
import random
import sys

def start_screen(screen):
    # Constants
    WIDTH, HEIGHT = 800, 600
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_SIZE = 30

    # Font for displaying the text
    font = pygame.font.Font(None, FONT_SIZE)

    # Fill the screen with the background color
    screen.fill(BLACK)

    # Introduction text
    intro_text = [
        "Welcome, Alien Abductor!",
        "You're behind on your weekly quota of abductions.",
        "Help the alien catch up by abducting targets on Earth!",
        "",
        "----------------------------------------------------------------------------------------------",
        "Move the UFO with ARROWS and", 
        "press SPACE to abduct cows with the track bean.",
        "----------------------------------------------------------------------------------------------",
        "",
        "Press any key to start the game...",
        "",
    ]

    # Render and display the introduction text
    y_position = HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        y_position += FONT_SIZE

    pygame.display.flip()

    # Wait for a key press to start the game
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_text_on_screen(screen, text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)

def game_over_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_text_on_screen(screen, "Game Over", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_text_on_screen(screen, "Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"You've completed all levels with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

# Load spaceship and cow images
ovni = pygame.image.load("ovni.png")
cow = pygame.image.load("cow.png")

# Resize images if needed
ovni = pygame.transform.scale(ovni, (50, 50))
cow = pygame.transform.scale(cow, (40, 40))

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

# List to store stars
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3),
          'color': LIGHT_BLUE} for _ in range(STAR_COUNT)]

# Grassy area at the bottom
grass_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)

# Level and Countdown Variables
current_level = 1
abduction_target = 10  # Initial target
countdown_timer = 60  # Initial countdown timer in seconds
current_score = 0  # New counter to track the score for the current level

# Counter to control the pace of target appearances
target_spawn_counter = 0
TARGET_SPAWN_RATE = max(30, 120 - (current_level * 90))  # Adjust the rate based on the current level

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

# Function to display the start screen
start_screen(screen)

# Main game loop
running = True
game_started = False  # Flag to track whether the game has started

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_started:
                game_started = True  # Set the flag to True to avoid calling start_screen repeatedly
                continue  # Skip the rest of the loop until the game has started
            elif event.key == pygame.K_SPACE:
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
        target_rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT - 50, 50, 50)
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
    screen.blit(ovni, player_rect)
    
    for target in targets:
        screen.blit(cow, target)

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
                current_score += 1
                score += 1

    info_line_y = 10  # Adjust the vertical position as needed
    info_spacing = 75  # Adjust the spacing as needed

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top left (next to the score)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the countdown timer in a red rectangle at the top left (next to the level)
    timer_text = font.render(f"Time: {int(countdown_timer)}", True, WHITE)
    timer_rect = timer_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, timer_rect.inflate(10, 5))
    screen.blit(timer_text, timer_rect)

    # Draw the targets to acquire for the current level in a gray rectangle at the top left (next to the timer)
    targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
    targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, GRAY, targets_rect.inflate(10, 5))
    screen.blit(targets_text, targets_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

     # Countdown Timer Logic
    countdown_timer -= 1 / FPS  # Decrease the timer based on the frame rate
    if countdown_timer <= 0:
        # Check if the player reached the abduction target for the current level
        if current_score < abduction_target:
            # Player didn't reach the abduction target, end the game
            game_over_screen(screen)
            running = False
        else:
            # Move to the next level
            current_level += 1
            if current_level <= 10:
                current_score = 0
                abduction_target = 10 * current_level
                countdown_timer = 60  # Reset the countdown timer for the next level
                # Reset the targets text for the next level
                targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
                targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))

    # Check if the player reached the abduction target for the current level
    if current_score >= abduction_target:
        # Move to the next level
        current_level += 1
        if current_level <= 10:
            current_score = 0
            abduction_target = 10 * current_level
            countdown_timer = 60  # Reset the countdown timer for the next level
            # Reset the targets text for the next level
            targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
            targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))
        else:
            victory_screen(screen)
            running = False

# Quit Pygame
pygame.quit()