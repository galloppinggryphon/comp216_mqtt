import logging
from threading import Thread
from typing import Any, Callable, Iterable

from app.api.helpers.bool_signal import BoolSignal

# Persistent register of used threads
# Lists should be thread-safe under normal circumstances
threads = []


class ThreadWorker:
    """
    Small utility to launch threads.
    """
    abort_signal: BoolSignal
    thread: Thread

    def __init__(self, fn: Callable, args: Iterable[Any] = [], background=False):
        self.thread_cleanup()

        # Start background thread
        self.thread = Thread(target=fn, daemon=background,
                             args=args)

        self.thread.start()

        threads.append(self.thread)
        logging.info(f'Started daemon thread: {self.thread.getName(), self.thread.isDaemon()}')


    def wait(self):
        self.thread.join()

    def is_alive(self):
        return self.thread.is_alive()

    def thread_cleanup(self):
        # Delete inactive threads
        # TODO: non-atomic operation, dunno how thread-safe this is
        for i in range(len(threads)):
            t = threads[i-1]
            if not t.is_alive():
                logging.info('Delete inactive thread %s', t.name)
                del threads[i-1]
