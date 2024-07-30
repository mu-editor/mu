# Ovoz sensor orqali Baramining tezligini boshqarish 

from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in3') < 30:
        n.motor_stop('right')
    else:
        n.motor_rotate('right', 'forward', 'in3')
        