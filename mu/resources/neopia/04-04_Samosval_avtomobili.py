from neopia import *

n =  Neosoco()
n.servo_reset_degree('out1')
while True:
    key = Keyboard.read()
    if key == '4':
        n.servo_rotate_by_degree('out1', 'forward', '20', '60')
    if key == '1':
        n.servo_rotate_by_degree('out1', 'forward', '20', '0')