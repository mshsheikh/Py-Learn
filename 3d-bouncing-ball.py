from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create a red ball
ball = Entity(model='sphere', color=color.red, scale=0.5, collider='sphere')
ball.velocity = Vec3(0, 0, 0)  # Initial velocity
ball.gravity = 1.5             # Strength of gravity
ball.bounce_damping = 0.8      # Energy loss on bounce

# Create ground
ground = Entity(model='plane', scale=10, texture='grass', collider='box')

def update():
    # Handle arrow key input for movement
    ball.velocity.x = held_keys['right arrow'] * 5 - held_keys['left arrow'] * 5
    ball.velocity.z = held_keys['up arrow'] * 5 - held_keys['down arrow'] * 5

    # Apply gravity
    ball.velocity.y -= ball.gravity * time.dt

    # Update position based on velocity
    ball.position += ball.velocity * time.dt

    # Check for collision with ground
    if ball.y < ground.y + 0.5:
        ball.y = ground.y + 0.5
        ball.velocity.y *= -ball.bounce_damping

# Set up camera
camera.position = (0, 15, -15)
camera.look_at(ball.position)

app.run()