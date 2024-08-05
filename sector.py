import time
import os


class Log:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append((time.time(), message))

    # this makes it so that the program starts at 0
    def __repr__(self):
        if len(self.messages) == 0:
            return ''
        start_time = self.messages[0][0]
        return '\n'.join([f'{(m[0] - start_time) * 1000} (ms): {m[1]}' for m in self.messages])

    # in ms
    def diff(self, i1, i2):
        return (self.messages[i2][0] - self.messages[i1][0]) * 1000


class ExtentLog:
    # extent states
    START = 0
    EXTENT = 1

    def __init__(self):
        self.extents = {}

    def start(self, extent_key):
        self.extents[extent_key] = (ExtentLog.START, time.time())

    def end(self, extent_key):
        extent = self.extents[extent_key]
        self.extents[extent_key] = (ExtentLog.EXTENT, time.time() - extent[1])

    def get_ms(self, key):
        return self.extents[key][1] * 1000

    def __repr__(self):
        return '\n'.join([f'{e}: {d[1] * 1000} (ms)' for e, d in self.extents.items() if d[0] == ExtentLog.EXTENT])

# the hypothesis we're testing here is that flushing takes much longer than just .write-ing.
def basic_sync_test():
    l = Log()
    l.add_message('opening file')
    f = open('tmp/test.dat', 'w')
    l.add_message('writing to file')
    f.write('asdf')
    l.add_message('syncing file')
    os.fsync(f.fileno())
    l.add_message('finished')
    print(l)


# the hypothesis here is that writing a sector worth of information vs
# less than a sector will take the same amount of time.
def sector_test():
    # averaging over 100 times
    k1 = 'f1 write and sync'
    k2 = 'f2 write and sync'
    # statically allocting these so that init-ing them doesn't mess
    # with our runtimes
    s1 = "meow"
    s2 = "mrow" * 100

    results1 = []
    results2 = []
    for i in range(1000):
        el = ExtentLog()
        f1 = open('tmp/test1', 'w')
        f2 = open('tmp/test2', 'w')

        el.start(k1)
        f1.write(s1)
        os.fsync(f1.fileno())
        el.end(k1)

        el.start(k2)
        f2.write(s2)
        os.fsync(f2.fileno())
        el.end(k2)

        f1.close()
        f2.close()
        results1.append(el.get_ms(k1))
        results2.append(el.get_ms(k2))
    results1_avg = sum(results1) / len(results1)
    results2_avg = sum(results2) / len(results2)
    print(results1_avg, results2_avg, results1_avg - results2_avg)

sector_test()
