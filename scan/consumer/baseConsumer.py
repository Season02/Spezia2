import threading
import abc

class base_consumer(object):
    def __init__(self):
        pass

    def get_thread(self, func, arg=None):
        th = self.core_thread(func, arg)
        th.daemon = True # 当主线程退出时子线程也退出
        th.start()

        return th

    class core_thread(threading.Thread):
        def __init__(self, func, arg):
            super().__init__()
            self.func = func
            self.arg = arg

        def run(self):
            if self.arg:
                self.func(self.arg)
            else:
                self.func()

    # def pri(self, val):
    #     print("2323" + " " + str(val))