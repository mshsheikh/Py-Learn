import pygame
import sys

pygame.init()

# Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")

# Colors
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        # Ball moves
        self.x += self.speed_x
        self.y += self.speed_y

        # Walls
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Ball (as Object)
red_ball = Ball(100, 100, 30, RED, 5, 4)
orange_ball = Ball(400, 300, 40, ORANGE, -4, 5)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update balls
    red_ball.update()
    orange_ball.update()

    # Draw everything
    screen.fill(BLACK)
    red_ball.draw()
    orange_ball.draw()

    # Display update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()