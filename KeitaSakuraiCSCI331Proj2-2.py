import threading
import random
import time

# 2.Modify the solution by including the necessary P and V operations in the code.
# If general P and V operations are not provided by the thread library then first implement P and V using binary
# semaphores (mutex lock or spin locks.)

BUFFER_SIZE = 10
ROUND = 20
buffer = [0] * BUFFER_SIZE
limit = ROUND
next_in = 0
next_out = 0
emptyBuffer = threading.Semaphore(BUFFER_SIZE)
occupiedBuffer = threading.Semaphore(0)
count = 0
done = False

def producer():
    global next_in, limit, done
    while not done:
        k1 = random.randint(1, BUFFER_SIZE // 2)
        for _ in range(k1):
            emptyBuffer.acquire()
            buffer[next_in] = 1
            next_in = (next_in + 1) % BUFFER_SIZE
            occupiedBuffer.release()
        print(f"Produced {k1} items")
        limit -= 1
        if limit <= 0:
            print("Producer exits system without any race problem")
            done = True
        time.sleep(random.uniform(0.1, 0.5))

def consumer():
    global next_out, limit, done
    while not done:
        time.sleep(random.uniform(0.1, 0.5))
        k2 = random.randint(1, BUFFER_SIZE // 2)
        for _ in range(k2):
            occupiedBuffer.acquire()
            value = buffer[next_out]
            if value != 1:
                print("Error: Consumer found unexpected value in buffer.")
            buffer[next_out] = 0
            next_out = (next_out + 1) % BUFFER_SIZE
            emptyBuffer.release()
        print(f"Consumed {k2} items")
        limit -= 1
        if limit <= 0:
            print("Consumer exits system without any race problem")
            done = True

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
