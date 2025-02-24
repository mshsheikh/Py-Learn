import pygame
import random

# Initializing
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Display dimensions
WIDTH = 600
HEIGHT = 400

# Game window
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the clock to control the game's frame rate
clock = pygame.time.Clock()

# Define snake block size and speed
BLOCK_SIZE = 10
SNAKE_SPEED = 15

# Define fonts for displaying messages
FONT_STYLE = pygame.font.SysFont("bahnschrift", 20)
SCORE_FONT = pygame.font.SysFont("comicsansms", 30)

# Load cherry image from a link
CHERRY_IMAGE_URL = "https://pngimg.com/d/cherry_PNG632.png"  # Replace with your image URL
import urllib.request
cherry_image_path = "cherry.png"
urllib.request.urlretrieve(CHERRY_IMAGE_URL, cherry_image_path)
cherry_image = pygame.image.load(cherry_image_path)
cherry_image = pygame.transform.scale(cherry_image, (BLOCK_SIZE, BLOCK_SIZE))

def display_score(score):
    """Displays the player's score on the screen."""
    value = SCORE_FONT.render(f"Score: {score}", True, YELLOW)
    game_window.blit(value, [10, 10])

def display_time(time_seconds):
    """Displays the elapsed time on the screen."""
    value = SCORE_FONT.render(f"Time: {time_seconds}s", True, YELLOW)
    game_window.blit(value, [WIDTH - 150, 10])

def draw_snake(block_size, snake_list):
    """Draws the snake on the screen."""
    for block in snake_list:
        pygame.draw.rect(game_window, GREEN, [block[0], block[1], block_size, block_size])

def display_message(msg, color):
    """Displays a message in the center of the screen."""
    message = FONT_STYLE.render(msg, True, color)
    game_window.blit(message, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    """Main function to run the Snake game."""
    game_over = False
    game_close = False

    # Initial position of the snake
    x = WIDTH / 2
    y = HEIGHT / 2

    # Change in position
    x_change = 0
    y_change = 0

    # Snake body (list of blocks)
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    # Cherry variables
    cherry_active = False
    cherry_x = None
    cherry_y = None
    cherry_spawn_time = 0
    CHERRY_DURATION = 30000  # 30 seconds in milliseconds

    # Time tracking
    start_time = pygame.time.get_ticks()

    while not game_over:
        while game_close:
            game_window.fill(BLACK)
            display_message('YOU LOST! Press, Q to Quit or C to Play Again.', RED)
            display_score(snake_length - 1)
            pygame.display.update()

            # Handle game over events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle movement events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Check for boundary collisions
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Update snake position
        x += x_change
        y += y_change

        # Draw background and food
        game_window.fill(BLACK)
        pygame.draw.rect(game_window, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Draw the snake
        draw_snake(BLOCK_SIZE, snake_list)

        # Display score and time
        display_score(snake_length - 1)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        display_time(elapsed_time)

        # Check if the snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            snake_length += 1

            # Spawn a cherry after eating food
            if not cherry_active:
                cherry_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
                cherry_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
                cherry_spawn_time = pygame.time.get_ticks()
                cherry_active = True

        # Handle cherry logic
        if cherry_active:
            current_time = pygame.time.get_ticks()
            if current_time - cherry_spawn_time <= CHERRY_DURATION:
                # Draw cherry image
                game_window.blit(cherry_image, (cherry_x, cherry_y))

                # Check if the snake eats the cherry
                if x == cherry_x and y == cherry_y:
                    snake_length += 20  # Add 20 points
                    cherry_active = False
            else:
                # Remove cherry if time exceeds 30 seconds
                cherry_active = False

        # Update the display
        pygame.display.update()

        # Control the game speed
        clock.tick(SNAKE_SPEED)

    # Quit pygame
    pygame.quit()
    quit()

# Run the game
if __name__ == "__main__":
    game_loop()
