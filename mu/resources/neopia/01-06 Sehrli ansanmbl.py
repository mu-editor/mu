# Ichki buzzer orqali yangrash

from neopia import *

n =  Neosoco()
while True:
    n.buzzer_by_port('in1')
    wait(200)
    n.buzzer_stop()