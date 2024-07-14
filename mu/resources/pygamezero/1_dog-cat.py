from pgzhelper import *

WIDTH = 480
HEIGHT = 270

dog = Actor('dog', (100, 150))
dog.scale = 0.5
cat = Actor('cat', (350, 150))
cat.scale = 0.5
cat.flip_x = True

def draw():
    screen.fill('white')
    dog.draw()
    cat.draw()

    dog.say_for_sec("Bow-wow", 2)
    cat.say_for_sec("Meow", 2)
    dog.say_for_sec("Good bye!", 2)
    cat.say_for_sec("See you!", 2)

