from pgzhelper import *

WIDTH = 960
HEIGHT = 540

robot = Actor('changyutgich', (WIDTH / 2, HEIGHT / 2))
robot.scale = 0.3
robot.angle = 90
robot.pen_init((WIDTH, HEIGHT))

def draw():
    screen.blit('pol', (0, 0))
    robot.pen_start(50, 'white')
    robot.pen_update()
    robot.draw()

def update():
    robot.move_forward(10)

    if robot.top < 0 or robot.right > WIDTH \
        or robot.bottom > HEIGHT or robot.left < 0:
        robot.move_back(10)
        robot.angle += 133


