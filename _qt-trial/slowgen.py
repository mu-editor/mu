import os, sys
import time
import random


for i in range(5):
    print("".join(random.sample("abcdefghijklmnopqrstuvwxyz", random.randint(3, 10))))
    time.sleep(10 * random.random())

