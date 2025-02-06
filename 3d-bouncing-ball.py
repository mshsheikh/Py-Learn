from ursina import *

app = Ursina()

# Create a red ball positioned ABOVE the ground
ball = Entity(model='sphere', color=color.red, scale=0.5, collider='sphere', position=(0, 5, 0))
ball.velocity = Vec3(0, 0, 0)  # Initial velocity
ball.gravity = 1.5             # Strength of gravity
ball.bounce_damping = 0.8      # Energy loss on bounce

# Create ground with proper collider
ground = Entity(model='plane', scale=10, texture='grass', collider='mesh')

def update():
    # Handle arrow key input for movement
    ball.velocity.x = held_keys['right arrow'] * 5 - held_keys['left arrow'] * 5
    ball.velocity.z = held_keys['up arrow'] * 5 - held_keys['down arrow'] * 5

    # Apply gravity
    ball.velocity.y -= ball.gravity * time.dt

    # Update position based on velocity
    ball.position += ball.velocity * time.dt

    # Proper collision check with ground
    if ball.intersects(ground).hit:
        # Reset position to ground level + ball radius
        ball.y = ground.y + ball.scale_y/2
        # Reverse and dampen vertical velocity
        ball.velocity.y *= -ball.bounce_damping

    # Make camera follow the ball
    camera.position = (ball.x - 5, 15, ball.z - 5)
    camera.look_at(ball.position)

app.run()
