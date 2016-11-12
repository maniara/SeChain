import os
import subprocess
import threading

'''
    2016/11/12
    ping test
    using thread pool & run as daemon
'''


class Pinger(object):
    status = {'alive': [], 'dead': []}
    hosts = []

    thread_count = 10

    lock = threading.Lock()

    '''
        return 0 if ping test is successful
    '''
    def ping(self, ip):
        ret = subprocess.call(['ping', '-n', '1', ip],
                              stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

        return ret == 0

    def pop_queue(self):
        ip = None

        self.lock.acquire()

        if self.hosts:
            ip = self.hosts.pop()

        self.lock.release()
        return ip

    def dequeue(self):
        while True:
            ip = self.pop_queue()

            if not ip:
                return None

            result = 'alive' if self.ping(ip) else 'dead'
            self.status[result].append(ip)

    '''
        start thread pool
        blocking method
    '''
    def start(self):
        threads = []

        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.setDaemon(True)
            t.start()
            threads.append(t)

        [t.join() for t in threads]

        return self.status
