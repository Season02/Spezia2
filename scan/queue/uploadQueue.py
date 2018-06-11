from .baseQueue import base_queue
import queue
import multiprocessing

class upload_queue(object):
    def __new__(cls, len=1):
        if not hasattr(cls, 'instance'):
            cls.instance = super(upload_queue, cls).__new__(cls)
            cls.instance.init(len)
        return cls.instance

    def init(self, len):
        try:
            manager = multiprocessing.Manager()
            self.queue = manager.Queue(len)
            # self.queue = queue.Queue(len)
            return True
        except Exception:
            pass

