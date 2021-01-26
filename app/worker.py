# Async worker
import time
from collections import deque


class Deque(deque):
    def call(self, method, args=(), kwargs={}):
        return [getattr(i, method)(*args, **kwargs) for i in self.copy()]


class Work(object):
    ins = {}

    def __new__(self, name):
        if name in self.ins:
            return self.ins[name]
        i = super().__new__(self)
        self.ins[name] = i
        return i

    def __init__(self, name):
        self.name = name
        self.workers = Deque()
        self.contents = deque()

    def __getitem__(self, index):
        return self.contents.__getitem__(index)

    def add(self, ctx):
        self.contents.append(ctx)

    def append(self, worker):
        ws = self.workers
        ws.append(worker)
        return len(ws) - 1

    def reset(self):
        self.contents = deque()
        self.workers.call('reset')

    def destroy(self):
        self.workers.call('destroy')
        self.ins.pop(self.name)
        del self

    def __len__(self):
        return len(self.contents)

    def __eq__(self, other):
        print('work eq call')
        return self.name == other.name


class Worker(object):

    def __init__(self, work):
        if not isinstance(work, Work):
            raise TypeError('work Must be a Work Instance')
        self._wp = work.append(self)
        self.work = work
        self._count = 0
        self.connected = True

    def iter(self):
        while True:
            r = next(self)
            if isinstance(r, bool):
                self.quit()
                break
            else:
                yield self.analyze(r)

    def destroy(self):
        self.connected = False

    def analyze(self, e):
        return e

    def reset(self):
        self._count = 0

    def quit(self):
        print("Quit")
        if self in self.work.workers:
            self.work.workers.remove(self)
        self.connected = False

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if not self.connected:
            return False
        c = self._count
        if len(self.work) > c:
            self._count += 1
            return self.work[c]
        w = self.work
        t = 0
        while len(w) <= c:
            if not self.connected:
                return False
            time.sleep(0.2 + t)
            t += 0.0001
            if t >= 1:
                print("Work time out!")
                return False
        self._count += 1
        return w[c]

    def __eq__(self, other):
        return self._wp == other._wp and self.work == other.work
