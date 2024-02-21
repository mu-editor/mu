from pgzhelper import *
import random, math

WIDTH = 960
HEIGHT = 540

hammer = Actor("o'yinchoq_bolg'a", (WIDTH / 2, HEIGHT / 2))
hammer.scale = 0.5
hammer.angle = 40

GAP_FROM_SCR = 50
mice = []
for _ in range(10):
    mouse = Actor("ko'rsichqon_1")
    mouse.anchor=('left', 'top')
    x = random.randint(GAP_FROM_SCR, WIDTH - mouse.width + GAP_FROM_SCR)
    y = random.randint(GAP_FROM_SCR, HEIGHT - mouse.height + GAP_FROM_SCR)
    mouse.pos = (x, y)
    mouse.scale = 0.5
    mice.append(mouse)

ball = 0
delayed_time = 0
random_mice = []

def draw():
    global random_mice, delayed_time
    screen.blit('dala', (0, 0))

    current_time = pygame.time.get_ticks()
    if current_time > delayed_time:
        random_mice = random.sample(mice, math.ceil(len(mice) / 2))
        delayed_time = current_time + 1000

    for mouse in random_mice:
        mouse.draw()
    hammer.draw()
    screen.draw.text('Ball: ' + str(ball), (20, 20), color='black')

def on_mouse_move(pos):
    hammer.centerx, hammer.centery = pos

def on_mouse_down():
    global ball

    animate(hammer, angle=75, tween='accelerate', duration=0.3, on_finished=animation_done)
    idx = hammer.collidelist_pixel(mice)
    if idx != -1:
        sounds.toi.play()
        mice.pop(idx)
        ball += 1

def animation_done():
    animate(hammer, angle=40, tween='accelerate', duration=0.3)

