import os
import time
import threading

from queue import Queue, Empty

# Default exception handler
def execption_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


class Worker(threading.Thread):

    def __init__(self, name, queue, result=None, wait_queue=False, sleep=0.5, callback=None,
        execption_handler=execption_handler):

        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.result = result if isinstance(result, Queue) else Queue()
        self.sleep = sleep
        self._abort = threading.Event()
        self._idle = threading.Event()
        self._pause = threading.Event()
        self.callback = callback
        self.execption_handler = execption_handler
        self.wait_queue = wait_queue


    def abort(self, block=True):
        self._abort.set()
        self.block(block)

    def aborted(self):
        return self._abort.is_set()

    def pause(self):
        self._pause.set()
        self._idle.set()

    def resume(self):
        self._pause.clear()
        self._idle.clear()

    def paused(self):
        return self._pause.is_set()

    def __del__(self):
        if not self.aborted():
            self.abort()

    def _pause_now(self):
        """ block the code for a while """
        while self.paused():
            time.sleep(self.sleep)

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(self.sleep)

    def run(self):
        while not self.aborted():
            try:
                func, args, kwargs = self.queue.get(timeout=0.5)
                self._idle.clear()
            except Empty:
                # the queue is empty.
                self._idle.set()
                # abort the thread if the queue is empty.
                if not self.wait_queue:
                    break
                continue
            except Exception as e:
                pass

            # the task is available to work with.
            try:
                r = func(*args, **kwargs)
                self.result.put(r)
                if self.callback:
                    self.callback(r)

            except Exception as e:
                self.execption_handler(self.name, e)
            finally:
                self.queue.task_done()

            # pause the thread is _pause flag is set
            self._pause_now()



class Pool:
    def __init__(self, max_workers=os.cpu_count() + 4, name=None, queue=None, wait_queue=True,
        result_queue=None, workers_sleep=0.5, callback=None, execption_handler=execption_handler):
        self.name = name
        self.max_worker = max_workers
        self.callback = callback
        self.workers_sleep = workers_sleep
        self.execption_handler = execption_handler

        self.queue = queue if isinstance(queue, Queue) else Queue()
        self.result_queue = result_queue if isinstance(result_queue, Queue) else Queue()
        self.wait_queue = wait_queue

        self.threads = []


    def start(self):
        # reinitialize values
        self.threads = []

        # create all threads
        for i in range(self.max_worker):
            self.threads.append(Worker(f'Worker_{i}_{self.name}', self.queue, self.result_queue, wait_queue=self.wait_queue, sleep=self.workers_sleep, callback=self.callback))

        # start all threads
        for t in self.threads:
            t.start()

        return True

    def is_alive(self):
        return any((t.is_alive() for t in self.threads))

    def is_idle(self):
        return False not in (t.idle() for t in self.threads)

    def is_done(self):
        return self.queue.empty()

    def shutdown(self, block=False):
        """ Abort all threads in the pool """
        for t in self.threads:
            t.resume() # the thread should be working to abort it.
            t.abort()
        self.block(block)
        self.result_queue = None


    def join(self, timeout=None):
        """ wait until all the queue tasks be completed """
        if timeout and self.is_alive():
            time.sleep(timeout)
        else:
            self.queue.join()

    def result(self, block=False):
        """ return result as generator """
        result = []
        if block and self.is_alive():
            self.join()
        try:
            while True:
                result.append(self.result_queue.get(False))
                self.result_queue.task_done()
        except:
            # the result_queue is emply
            pass

        return result

    def __del__(self):
        self.shutdown()

    def is_paused(self):
        return False not in ( t.paused() for t in self.threads )

    def pause(self, timeout=0, block=False):
        for t in self.threads:
            t.pause()
        if timeout:
            time.sleep(timeout)
            self.resume()
        return True

    def resume(self, block=False):
        for t in self.threads:
            t.resume()
        return True

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(0.5)

    def count(self):
        return len(self.threads)


    def update(self, n, block=False):

        # create necissary threads
        need = n - self.count()
        if need > 0:
            # create more threads
            for _ in range(need):
                t = Worker(f'Worker_{(self.count())} ({self.name})', self.queue, self.result_queue, wait_queue=self.wait_queue, callback=self.callback)               
                t.start()
                self.threads.append(t)

        elif need < 0:
            need = abs(need)
            # delete some threads
            threads = []
            for _ in range(need):
                t = self.threads.pop()
                t.resume() # the thread should be working to abort it.
                t.abort()
                threads.append(t)

            # block until the extra threads dead.
            while block and any(( t.is_alive() for t in threads )):
                time.sleep(0.5)




