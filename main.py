# -*- coding: utf-8 -*-
"""A stream manager template
"""

import time, threading
import pprint


class Stream():
    """Stream.
    """

    def __init__(self):
        """__init__.
        """
        self.dead_time = time.time() + 100
        self.is_opened = True
        self.buf = 0
        self.listener_thread = None
        self.lock = threading.Lock()

    def run(self):
        """run.
        """

        def listener(self):
            """listener.

            Args:
                self:
            """
            while self.is_opened and time.time() < self.dead_time:
                time.sleep(1)
                self.lock.acquire()
                self.buf += 1
                self.lock.release()

        self.listener_thread = threading.Thread(name="Stream",
                                                target=listener,
                                                args=(self,))
        self.listener_thread.start()

    def gen(self):
        """gen.
        """
        while True:
            self.lock.acquire()
            res = self.buf
            self.lock.release()
            yield res

    def close(self):
        """close.
        """
        self.is_opened = False


class StreamManager():
    """StreamManager.
    """

    def __init__(self):
        """__init__.
        """
        self.streams = {}
        self.thread = self.worker_thread()
        self.thread.start()
    def worker_thread(self):
        """run.
        """

        def worker(self):
            """worker.

            Args:
                self:
            """
            while True:
                time.sleep(1)
                key_to_remove = []
                for key in self.streams:
                    stream = self.streams[key]
                    if not stream.is_opened and not stream.listener_thread.is_alive(
                    ):
                        key_to_remove.append(key)
                    if stream.dead_time <= time.time():
                        stream.close()
                for key in key_to_remove:
                    dead_stream = self.streams.pop(key)
                    del dead_stream

                print("streams: ", self.streams)

        return threading.Thread(target=worker, name="Stream Manager", args=(self,))

    def create_stream(self):
        """create_loop.
        """
        stream = Stream()
        self.streams[id(stream)] = stream
        return stream


class ThreadPrinter():
    """thread_manager.
    """

    def __init__(self):
        self.run()
    def run(self):
        """run.
        """

        def worker():
            """worker.
            """
            while True:
                time.sleep(1)
                # pprint.pprint(threading.enumerate())

        threading.Thread(target=worker, name="Thread Manager").start()


if __name__ == "__main__":
    sm = StreamManager()
    tp = ThreadPrinter()
    stream = sm.create_stream()
    stream.run()
    for i in range(70):
        time.sleep(0.07)
        next(stream.gen())
    time.sleep(3)
    stream.close()
