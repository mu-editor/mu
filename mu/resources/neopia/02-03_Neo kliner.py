from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in1') < 20:
        n.motor_rotate('both', 'forward', '50')
    else:
        n.motor_stop('both')