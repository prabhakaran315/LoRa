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
    amp = random.randint(-32768, 32767)
    vol = random.randint(-32768, 32767)
    ran = random.randint(-32768, 32767)
    print("amp : ",amp)
    print("vol : ",vol)
    print("ran : ",ran)
    amp_bytes = amp.to_bytes(2, byteorder='big', signed=True)
    vol_bytes = vol.to_bytes(2, byteorder='big', signed=True)
    ran_bytes = ran.to_bytes(2, byteorder='big', signed=True)
    counter += 1
    
    data = amp_bytes + vol_bytes + ran_bytes

    counter += 1
    #data = bytes([255]) + bytes([255]) + bytes([18]) + bytes([255]) + bytes([255]) + bytes([12]) + int(readings).encode() + int(counter).encode()
    #print("values : ", data)
    node.send(data)
    time.sleep(0.2)

    timer_task = Timer(5, send_data)
    timer_task.start()


old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
node = sx1262.sx126x(serial_num = "/dev/ttyAMA0",freq=915,addr=0,power=22,rssi=True,air_speed=2400,relay=False)
send_data()
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
