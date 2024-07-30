from neopia import *

n =  Neosoco()
while True:
    if n.get_value('in1') == 255:
        n.led_on('out1', '100')
    else:
        n.led_off('out1')