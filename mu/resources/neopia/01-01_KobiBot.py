from neopia import *

n =  Neosoco()

# LEDni yoqib 1 soniyadan keyin o'chirish
n.led_on('out1','100')
wait(1000) # milisekund orqali hisoblanadi


# Takrorlab miltiratish
while True:
    n.led_on('out1','100')
    wait(1000)
    n.led_off('out1')
    wait(1000)