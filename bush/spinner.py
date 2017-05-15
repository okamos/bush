import sys
import time
import threading


class Spinner(object):
    def __init__(self):
        self.__index = 3
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def __next(self):
        spinner = '|/-\\'
        self.__index += 1
        if self.__index > 3:
            self.__index = 0
        return spinner[self.__index]

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()
        sys.stdout.write('\b')

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(self.__next())
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
