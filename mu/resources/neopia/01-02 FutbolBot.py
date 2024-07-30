from neopia import *

n =  Neosoco()
while True:
  key = Keyboard.read()
  if key == Keyboard.UP:
    n.motor_rotate('both', 'forward', '10')
  elif key == Keyboard.DOWN:
    n.motor_rotate('both', 'backward', '10')
  elif key == Keyboard.LEFT:
    n.motor_rotate('both', 'left', '10')
  elif key == Keyboard.RIGHT:
    n.motor_rotate('both', 'right', '10')
  elif key == ' ':
    n.motor_stop('both')
