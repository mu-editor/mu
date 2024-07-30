from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in1') < 80 and n.get_value('in2') < 80:
        n.servo_stop('out1')
        n.motor_stop('both')
    elif n.get_value('in1') > 80 and n.get_value('in2') > 80:
        n.servo_stop('out1')
        n.motor_rotate('both', 'backward', '40')
    elif n.get_value('in1') > 80 and n.get_value('in2') < 80:
        n.servo_rotate('out1', 'forward', '10')
        n.motor_rotate('both', 'forward', '30')
    elif n.get_value('in1') < 80 and n.get_value('in2') > 80:
        n.servo_rotate('out1', 'backward', '10')
        n.motor_rotate('both', 'forward', '30')
