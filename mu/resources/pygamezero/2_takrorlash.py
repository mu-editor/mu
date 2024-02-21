from pgzhelper import *

WIDTH = 480
HEIGHT = 270

barg = Actor('pushti_barg', (WIDTH / 2, HEIGHT / 2), anchor=('middle', 'bottom'))
barg.scale = 0.5

def draw():
    barg.draw()

def update():
    barg.angle += 60
