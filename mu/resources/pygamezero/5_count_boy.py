from pgzhelper import *

WIDTH = 960
HEIGHT = 540

boy = Actor('boy_1', (WIDTH / 2, HEIGHT / 2))
boy.images = ['boy_1', 'boy_2', 'boy_3']

times = 0
pressed = False

def draw():
    screen.fill('white')
    boy.draw()
    screen.draw.text('Times: ' + str(times), (20, 20), color='black')

def update():
    global times, pressed
    if pressed:
        if boy.next_image() == 0:
            times += 1
            pressed = False

def on_mouse_down():
    global pressed
    pressed = True