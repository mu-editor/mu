from pgzhelper import *

WIDTH = 960
HEIGHT = 540

robot = Actor('cleaner', (WIDTH / 2, HEIGHT / 2))
robot.scale = 0.3
robot.angle = 90
robot.brush_init((WIDTH, HEIGHT), 50, 'white')

def draw():
    screen.blit('floor', (0, 0))
    robot.brush_draw()
    robot.draw()

def update():
    robot.move_forward(10)

    if robot.top < 0 or robot.right > WIDTH \
        or robot.bottom > HEIGHT or robot.left < 0:
        robot.move_back(10)
        robot.angle += 133


