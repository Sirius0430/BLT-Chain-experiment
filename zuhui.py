import threading

n = 0
lock = threading.Lock()


def add():
    global n, lock
    for i in range(1000000):
        # lock.acquire()
        n = n + 1
        # lock.release()


def sub():
    global n, lock
    for i in range(1000000):
        # lock.acquire()
        n = n - 1
        # lock.release()


if __name__ == "__main__":
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=sub)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("n的值为:", n)
