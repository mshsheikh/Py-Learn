from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina import Ursina, Entity, held_keys, time, Vec3, lerp, color, Circle, camera

app = Ursina()

# Configure window
window.title = 'Bouncing Ball Physics'
window.borderless = False
window.fullscreen = False

# Ball with RIGIDBODY
ball = Entity(
    model='sphere',
    color=color.red,
    scale=0.5,
    collider='sphere',
    position=(0, 5, 0),
    shader=basic_lighting_shader,
    mass=1.0,
    physics=True  # Physics engine ON
)
ball.velocity = Vec3(0, 0, 0)
ball.speed = 8
ball.bounce_damping = 0.7

# Thicker ground with BOX COLLIDER
ground = Entity(
    model='cube',
    scale=(20, 1, 20),
    texture='grass',
    collider='box',
    position=(0, -100, 0),  # Lower position with thickness
    shader=basic_lighting_shader,
    eternal=True
)

# Shadow
shadow = Entity(
    model=Circle(radius=0.3),
    color=color.black33,
    scale=0.6,
    rotation_x=90,
    eternal=True
)

# Configure camera
camera.position = (0, 15, -15)
camera.fov = 90

def update():
    # Horizontal movement input
    move_dir = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    ).normalized()

    # Apply horizontal movement directly to position (not velocity)
    ball.x += move_dir.x * ball.speed * time.dt
    ball.z += move_dir.z * ball.speed * time.dt

    # Physics-based vertical movement
    if not ball.intersects(ground).hit:
        ball.velocity.y -= 9.81 * time.dt  # Realistic gravity
    else:
        # Reset position when touching ground
        ball.y = ground.y + ground.scale_y/2 + ball.scale_y/2
        ball.velocity.y *= -ball.bounce_damping
        if abs(ball.velocity.y) < 0.2:
            ball.velocity.y = 0

    # Apply vertical movement
    ball.y += ball.velocity.y * time.dt

    # Shadow updates
    shadow.enabled = ball.intersects(ground).hit
    if shadow.enabled:
        shadow.position = (ball.x, ground.y + 0.1, ball.z)
        shadow.scale = 0.6
        shadow.color = color.black33

    # Camera follow
    camera.look_at(ball.position)
    camera.position = lerp(camera.position, ball.position + (0, 15, -15), time.dt * 5)

def input(key):
    if key == 'space' and ball.intersects(ground).hit:
        ball.velocity.y = 4  # Jump impulse

app.run()
