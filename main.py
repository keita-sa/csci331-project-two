import threading
import random
import time
import sys

# 1. Experiment with different values of n, k, and t until a race condition is observed.

buffer = [0] * 100
next_in = 0
next_out = 0
count = 0

def producer():
    global next_in
    while True:
        k1 = random.randint(1, len(buffer) // 3)  # random k1
        # write k1 data to buffer, regardless if buffer is full or not
        for i in range(k1):
            buffer[(next_in + i) % len(buffer)] += 1
        next_in = (next_in + k1) % len(buffer)
        time.sleep(random.random())  # random sleep time

def consumer():
    global next_out, count
    while True:
        time.sleep(random.random())  # sleep random time interval
        k2 = random.randint(1, len(buffer) // 3)  # random k2
        for i in range(k2):
            data = buffer[(next_out + i) % len(buffer)]
            if data > 1:
                print("Race condition detected! Consumer too slow")
                sys.exit(1)
            elif data == 0:
                print("Race condition detected! Producer too slow")
                sys.exit(1)
            else:
                buffer[(next_out + i) % len(buffer)] = 0  # clear buffer
        next_out = (next_out + k2) % len(buffer)
        count += 1
        print(f"Round {count} no race condition detected yet")

# Create producer thread
t1 = threading.Thread(target=producer)

# Create consumer thread
t2 = threading.Thread(target=consumer)

# Start both threads
t1.start()
t2.start()

# Join both threads
t1.join()
t2.join()
