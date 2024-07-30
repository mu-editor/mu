# Masofa sensor orqali to’siqdan qochish dasturi

from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in2') <= 7:
        n.motor_move('backward')
        wait(500)
        n.motor_stop('both')
        n.motor_move('left')
        wait(1000)
        n.motor_stop('both')
    else:
        n.motor_rotate('both', 'forward', '50')

