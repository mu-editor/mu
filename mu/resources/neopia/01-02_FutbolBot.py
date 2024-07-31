from neopia import *

n =  Neosoco()
def on_press(key): 
  if key == Keyboard.UP:
    n.motor_rotate('both', 'forward', '10')
  elif key == Keyboard.DOWN:
    n.motor_rotate('both', 'backward', '10')
  elif key == Keyboard.LEFT:
    n.motor_rotate('both', 'left', '10')
  elif key == Keyboard.RIGHT:
    n.motor_rotate('both', 'right', '10')
  elif key == Keyboard.SPACE:
    n.motor_stop('both')
  elif key == Keyboard.ESC:
    return False

Keyboard.read(on_press)