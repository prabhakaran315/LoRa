import RPi.GPIO as GPIO
import serial
import time


class SX126x:
    def __init__(self, serial_num="/dev/ttyAMA0", freq=915, my_addr=1, power=22, rssi=False):
        self.M0 = 22
        self.M1 = 27
        self.serial_n = serial_num
        self.freq = freq
        self.my_addr = my_addr
        self.power = power
        self.rssi = rssi
        self.ser = serial.Serial(serial_num, 9600)
        self.ser.flushInput()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.M0, GPIO.OUT)
        GPIO.setup(self.M1, GPIO.OUT)
        GPIO.output(self.M0, GPIO.LOW)
        GPIO.output(self.M1, GPIO.HIGH)
        time.sleep(0.1)

    def set_config(self):
        # Configure LoRa module settings
        config_bytes = [
            0xC2,                      # Configuration register
            (self.my_addr >> 8) & 0xFF,  # High byte of my address
            self.my_addr & 0xFF,          # Low byte of my address
            # Add other configuration bytes here...
            # Example: frequency, power level, modulation, etc.
        ]
        self.ser.write(bytes(config_bytes))
        time.sleep(0.2)
        response = self.ser.read(self.ser.inWaiting())
        if len(response) > 0 and response[0] == 0xC1:
            print("Configuration successful")
        else:
            print("Configuration failed")

    def send(self, data, destination_address):
        GPIO.output(self.M1, GPIO.LOW)
        GPIO.output(self.M0, GPIO.LOW)
        time.sleep(0.5)
        # Prepare data packet with destination address
        packet = bytes([destination_address]) + data
        print(packet)
        self.ser.write(packet)
        time.sleep(0.5)

    def receive(self):
        if self.ser.inWaiting() > 0:
            received_data = self.ser.read(self.ser.inWaiting())
            return received_data

# Initialize and configure each LoRa module
lora1 = SX126x(serial_num="/dev/ttyAMA0", freq=915, my_addr=1, power=22, rssi=False)
lora2 = SX126x(serial_num="/dev/ttyAMA0", freq=915, my_addr=2, power=22, rssi=False)
lora3 = SX126x(serial_num="/dev/ttyAMA0", freq=915, my_addr=3, power=22, rssi=False)

lora1.set_config()
lora2.set_config()
lora3.set_config()
while True:
# Send data from lora1 to lora2
    data = b"Hello from lora1"
    destination_address = 2
    lora1.send(data, destination_address)

# Receive data on lora2
while True:
    received_data = lora2.receive()
    print("Received data on lora2:", received_data)

# Send data from lora3 to lora2
data_to_send = b"Hello from lora3"
destination_address = 2
lora3.send(data_to_send, destination_address)

# Receive data on lora2
received_data = lora2.receive()
print("Received data on lora2:", received_data)
