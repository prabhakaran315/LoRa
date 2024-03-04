import sys
import sx1262
import threading
import time
import select
import termios
import tty
from threading import Timer

import random
global counter
import array
counter=0
#prabha
def send_data():
    global timer_task
    global counter
    amp = [31, 22, 34, 12, 14]
    vol = [32, 23, 35, 13, 15]
    ran = [33, 24, 36, 14, 16]
    counter += 1
    print("amp : ",amp)
    print("vol : ",vol)
    print("ran : ",ran)
    print("Counter : ", counter)
    amp_bytes = b"".join(x.to_bytes(2, byteorder='big', signed=True) for x in amp)
    vol_bytes = b"".join(x.to_bytes(2, byteorder='big', signed=True) for x in vol)
    ran_bytes = b"".join(x.to_bytes(2, byteorder='big', signed=True) for x in ran)
    con_bytes = counter.to_bytes(2, byteorder='big', signed=True)
    #amp_bytes = amp.to_bytes(2, byteorder='big', signed=True)
    #vol_bytes = vol.to_bytes(2, byteorder='big', signed=True)
    #ran_bytes = ran.to_bytes(2, byteorder='big', signed=True)

    
    data = amp_bytes + vol_bytes + ran_bytes + con_bytes
    #print(data)
    #counter += 1
    #data = bytes([255]) + bytes([255]) + bytes([18]) + bytes([255]) + bytes([255]) + bytes([12]) + int(readings).encode() + int(counter).encode()
    #print("values : ", data)
    node.send(data)
    time.sleep(0.2)

    timer_task = Timer(5, send_data)
    timer_task.start()


#old_settings = termios.tcgetattr(sys.stdin)
#tty.setcbreak(sys.stdin.fileno())
node = sx1262.sx126x(serial_num = "/dev/ttyAMA0",freq=915,addr=0,power=22,rssi=True,air_speed=62500,relay=False)
send_data()
'''
while True:
    node.receive()
'''
try:
    time.sleep(1)
    seconds = 5
    while True:

        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)
            sys.stdout.flush()
        node.receive()
except:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
