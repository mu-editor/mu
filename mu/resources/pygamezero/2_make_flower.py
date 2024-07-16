from pgzhelper import *

WIDTH = 480
HEIGHT = 270

leaf = Actor('pink_leaf', (WIDTH / 2, HEIGHT / 2), anchor=('middle', 'bottom'))
leaf.scale = 0.5

def draw():
    for _ in range(6):
        leaf.draw()
        leaf.angle += 60