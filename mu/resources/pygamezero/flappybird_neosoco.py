from pgzhelper import *
from neopia import *
import random

TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708

GRAVITY = 0.3
drop_speed = 0
bird_alive = True

GAP = 140  # Gap between pipes
PIPE_SPEED = -3

score = 0

# Create actors
flappy_bird = Actor('bird1', (75, 350))
flappy_bird.images = ['bird0', 'bird1', 'bird2']
flappy_bird.fps = 10

top_pipe = Actor('top', (350,0))
bottom_pipe = Actor('bottom', (350, top_pipe.height + GAP))

# Create Neosoco obj.
n = Neosoco()


def draw():
    screen.blit('background', (0, 0))
    flappy_bird.draw()
    top_pipe.draw()
    bottom_pipe.draw()

    screen.draw.text(
        str(score),
        color = 'white',
        midtop = (WIDTH/2, 10),
        fontsize = 70,
        shadow = (1, 1)
    )

# Create random pipe
def reset_pipes():
    random_y = random.randint(-100, 100)
    top_pipe.y = random_y
    bottom_pipe.y = top_pipe.height + GAP + random_y
    top_pipe.x = WIDTH
    bottom_pipe.x = WIDTH

def update():
    global drop_speed, bird_alive, score
    drop_speed += GRAVITY
    flappy_bird.y += drop_speed
    if bird_alive == True:
        flappy_bird.animate()

    top_pipe.x += PIPE_SPEED
    bottom_pipe.x += PIPE_SPEED

    # Seamless pipes
    if top_pipe.right < 0 or bottom_pipe.right < 0:
        reset_pipes()
        if bird_alive == True:
            score += 1

    # Check collision between bir and pipes
    if flappy_bird.colliderect(top_pipe) or flappy_bird.colliderect(bottom_pipe):
        flappy_bird.image = "birddead"
        bird_alive = False

    # Restart a game
    if flappy_bird.y > HEIGHT or flappy_bird.y < 0:
        flappy_bird.image = "bird1"
        bird_alive = True
        flappy_bird.center = (75, 350)
        drop_speed = 0
        reset_pipes()
        score = 0
        n.led_off()

    if n.get_value() > 50:  # default port: IN1
        n.led_on()  # default port: OUT1
        wait(20)
        on_mouse_down()

# When mouse is pressed
def on_mouse_down():
    global drop_speed
    if bird_alive == True:
        drop_speed = -3.5
        n.led_off()
