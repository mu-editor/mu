from pgzhelper import *

WIDTH = 960
HEIGHT = 540

bola = Actor('bola_1', (WIDTH / 2, HEIGHT / 2))
bola.images = ['bola_1', 'bola_2', 'bola_3']

marta = 0
pressed = False

def draw():
    screen.fill('white')
    bola.draw()
    screen.draw.text('Marta: ' + str(marta), (20, 20), color='black')

def update():
    global marta, pressed
    if pressed:
        if bola.next_image() == 0:
            marta += 1
            pressed = False

def on_mouse_down():
    global pressed
    pressed = True
