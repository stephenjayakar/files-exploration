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
    l = Log()
    # statically allocting these so that init-ing them doesn't mess
    # with our runtimes
    s1 = "meow"
    s2 = "mrow" * 100

    l.add_message('opening file 1')
    f1 = open('tmp/test1', 'w')
    l.add_message('opening file 2')
    f2 = open('tmp/test2', 'w')
    l.add_message('writing file 1')
    f1.write(s1)
    l.add_message('syncing file 1')
    os.fsync(f1.fileno())
    l.add_message('writing file 2')
    f2.write(s2)
    l.add_message('syncing file 2')
    os.fsync(f2.fileno())
    l.add_message('finished')
    f1.close()
    f2.close()
    print(l)
    return l


l = sector_test()
