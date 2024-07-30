from neopia import *

n =  Neosoco()

while True:
    while n.get_value('in3') > 50:
      continue
    while n.get_value('in3') <= 50:
      continue

    n.motor_rotate('both', 'left', '50')
    wait(3000)
    n.motor_stop('both')