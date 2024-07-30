from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in1') and n.get_value('in2') > 40:
        n.motor_rotate('both', 'forward', '30')
    else:
        if n.get_value('in1') <= 40:
            n.motor_stop('left')
        if n.get_value('in2') <= 40:
            n.motor_stop('right')
