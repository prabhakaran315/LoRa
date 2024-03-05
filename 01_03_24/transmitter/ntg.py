import time
counter=0
while True:
    counter = (counter + 1) % 256
    print(counter)
    time.sleep(0.2)