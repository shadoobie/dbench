__author__ = 'shadoobie'

import time
'''apparently perf_counter is not available in Python 2.7 but clock and time are.
at this time i do not know what is best here, but will press on.'''
class Timer:
    def __init__(self, func=time.clock):
                self.elapsed = 0.0
                self._func = func
                self._start = None
    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

