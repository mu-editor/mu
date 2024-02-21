from pgzhelper import *

WIDTH = 480
HEIGHT = 270

kuchuk = Actor('kuchuk', (100, 150))
kuchuk.scale = 0.5
mushuk = Actor('mushuk', (350, 150))
mushuk.scale = 0.5
mushuk.flip_x = True

def draw():
    screen.fill('white')
    kuchuk.draw()
    mushuk.draw()

    kuchuk.say_for_sec("Vov Vov", (200, 20), 2, color='black', background='white')
    mushuk.say_for_sec("Miyov", (200, 20), 2, color='black', background='white')
    kuchuk.say_for_sec("Yashi boring", (200, 20), 2, color='black', background='white')
    mushuk.say_for_sec("Xayr. Salomat bo'ling", (200, 20), 2, color='black', background='white')

