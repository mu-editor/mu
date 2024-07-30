# Klaviatura orqali Baramining tezligini boshqarish

from neopia import *

n =  Neosoco()
while True:
    key = Keyboard.read()
    if key == '0':
        n.motor_stop('right')
    elif key == '1':
        n.motor_rotate('right', 'forward', '10')
    elif key == '2':
        n.motor_rotate('right', 'forward', '50')
    elif key == '3':
        n.motor_rotate('right', 'forward', '100')