from pgzhelper import *
import random

WIDTH = 960
HEIGHT = 540

hammer = Actor('toy_hammer', (WIDTH / 2, HEIGHT / 2))
hammer.scale = 0.5
hammer.angle = 40

score = 0
hammer_pressed = False

GAP_FROM_SCR = 50
moles = []
for _ in range(6):
    mole = Actor('mole')
    mole.anchor = ('left', 'top')
    x = random.randint(GAP_FROM_SCR, WIDTH - mole.width + GAP_FROM_SCR)
    y = random.randint(GAP_FROM_SCR, HEIGHT - mole.height + GAP_FROM_SCR)
    mole.pos = (x, y)
    mole.scale = 0.5
    mole.visible = False
    moles.append(mole)


def draw():
    global score
    screen.blit('field', (0, 0))

    for mole in moles:
        if mole.visible: 
            mole.draw()
        if hammer_pressed and mole.visible and mole.collide_pixel(hammer):
            sounds.toi.play()
            moles.remove(mole)
            score += 1

    hammer.draw()
    screen.draw.text('Score: ' + str(score), (20, 20), color='black')


def update():
    if random.randint(0, 10) == 0:
        if len(moles) != 0:
            mole_list = random.sample(moles, 1)
            mole_list[0].visible = not mole_list[0].visible
        else:
            game.exit()


def on_mouse_move(pos):
    hammer.centerx, hammer.centery = pos


def on_mouse_down():
    global hammer_pressed
    hammer_pressed = True
    animate(hammer, angle=75, tween='accelerate', duration=0.1, on_finished=animation_done)
    

def animation_done():
    global hammer_pressed
    animate(hammer, angle=40, tween='accelerate', duration=0.1)
    hammer_pressed = False

