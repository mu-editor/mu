from neopia import *

n =  Neosoco()
n.servo_reset_degree('out1')
n.motor_rotate('both', 'forward', '40')
while True:
    if n.get_value('in1') > 20 and n.get_value('in2') > 20: 
        n.servo_rotate_by_degree('out1', 'forward', '50', '20')
        wait(500)
    if n.get_value('in1') <= 20 and n.get_value('in2') <= 20: 
        if n.get_value('in2') > 0:
            n.servo_rotate_by_degree('out1', 'backward', '50', '20')
            wait(500)        