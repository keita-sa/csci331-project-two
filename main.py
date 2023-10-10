import threading
import time
import random

# Constants
n = 10  # Buffer size
buffer = [0] * n  # Initialize buffer
next_in = 0
next_out = 0

# Semaphores
mutex = threading.Semaphore(1)
empty = threading.Semaphore(n)
full = threading.Semaphore(0)

# Producer thread
def producer():
    global next_in
    while True:
        k1 = random.randint(1, n)  # Burst size
        time.sleep(random.uniform(0, 1))  # Sleep for a random duration
        empty.acquire()
        mutex.acquire()
        for i in range(k1):
            buffer[(next_in + i) % n] = 1
        next_in = (next_in + k1) % n
        mutex.release()
        full.release()

# Consumer thread
def consumer():
    global next_out
    while True:
        t2 = random.uniform(0, 1)  # Sleep for a random duration
        time.sleep(t2)
        k2 = random.randint(1, n)  # Burst size
        mutex.acquire()
        for i in range(k2):
            data = buffer[(next_out + i) % n]
            if data > 1:
                print("Race condition detected!: Consumer too slow.")
                exit(1)
            elif data == 0:
                print("Race condition detected!: Producer too slow.")
                exit(1)
            else:
                buffer[(next_out + i) % n] = 0
        next_out = (next_out + k2) % n
        mutex.release()
        empty.release()

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for threads to finish (you can add a termination condition)
producer_thread.join()
consumer_thread.join()
