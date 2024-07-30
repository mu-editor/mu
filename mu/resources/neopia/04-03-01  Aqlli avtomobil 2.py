from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in2') <= 10:
        n.motor_stop('both')
        n.servo_reset_degree('out3')
        wait(100)
        n.servo_rotate_by_degree('out3', 'forward', '100', '90')
        wait(1000)
        chap_m = n.get_value('in2')
        n.servo_rotate_by_degree('out3', 'backward', '100', '90')
        wait(1000)
        ong_m = n.get_value('in2')
        n.servo_rotate_by_degree('out3', 'forward', '100', '0')
        wait(1000)
        if chap_m > ong_m:
            n.motor_rotate('both', 'left', '50')
            wait(1000)
        else:
            n.motor_rotate('both', 'right', '50')
            wait(1000)
    else:
        n.motor_rotate('both', 'forward', '50')
