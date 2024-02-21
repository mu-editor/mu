from pgzhelper import *

WIDTH = 960
HEIGHT = 540

drawing = False

qalam = Actor('qalam', (WIDTH / 2, HEIGHT / 2), anchor=('left', 'bottom'))
qalam.scale = 0.3
qalam.pen_init((WIDTH, HEIGHT))
eraser = Actor("o'chirg'ich", (900, 50))
eraser.scale = 0.5

def draw():
    screen.fill('white')
    if drawing:
        qalam.pen_start(5, 'blue')
    else:
        qalam.pen_stop()
    qalam.pen_update()
    qalam.draw()
    eraser.draw()

def on_mouse_move(pos):
    qalam.left, qalam.bottom = pos

def on_mouse_down(pos):
    global drawing
    drawing = True

    if eraser.collidepoint_pixel(pos):
        qalam.pen_clear()

def on_mouse_up():
    global drawing
    drawing = False
