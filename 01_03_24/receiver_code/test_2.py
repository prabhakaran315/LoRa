import sys
import sx1262_1
import threading
import time
import select
import termios
import tty

def receive_1():

    #data_1 = sx1262_1.sx126x
    data_2 = node.receive()
    if data_2:
        amp_bytes = data_2[0:10]
        vol_bytes = data_2[10:20]
        ran_bytes = data_2[20:30]
        con_bytes = data_2[30:32]
        # Convert bytes back to integers
        amp = [int.from_bytes(amp_bytes[i:i + 2], byteorder='big', signed=True) for i in range(0, len(amp_bytes), 2)]
        vol = [int.from_bytes(vol_bytes[i:i + 2], byteorder='big', signed=True) for i in range(0, len(vol_bytes), 2)]
        ran = [int.from_bytes(ran_bytes[i:i + 2], byteorder='big', signed=True) for i in range(0, len(ran_bytes), 2)]
        con = int.from_bytes(con_bytes, byteorder='big', signed=True)
        #amp = int.from_bytes(amp_bytes, byteorder='big', signed=True)
        #vol = int.from_bytes(vol_bytes, byteorder='big', signed=True)
        #ran = int.from_bytes(ran_bytes, byteorder='big', signed=True)

        print("Encoded values : ", data_2)
        print("amp:", amp)
        print("vol:", vol)
        print("ran:", ran)
        print("Counter : ", con)

        response_data = bytes([255]) + bytes([255]) + bytes([18]) + bytes([255]) + bytes([255]) + bytes([12]) + b"Response message"
        node.send(response_data)
    else:
        pass
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

node = sx1262_1.sx126x(serial_num = "/dev/ttyAMA0",freq=915,addr=0,power=22,rssi=True,air_speed=2400,relay=False)

while True:
    receive_1()

'''try:
    time.sleep(1)
    seconds = 5
    while True:
        receive_1()

except:

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)'''
