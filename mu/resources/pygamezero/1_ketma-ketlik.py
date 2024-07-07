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

    kuchuk.say_for_sec("Vov Vov", 2)
    mushuk.say_for_sec("Miyov", 2)
    kuchuk.say_for_sec("Yashi boring", 2)
    mushuk.say_for_sec("Xayr. Salomat bo'ling", 2)

