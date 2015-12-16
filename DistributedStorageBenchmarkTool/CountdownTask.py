__author__ = 'shadoobie'
import time

class CountdownTask:

    def __init__(self, log, sock, clientName):
        self.log = log
        self.sock = sock
        self.flood("CountdownTask for heartbeat has been instantiated but not yet started.")
        self.clientName = clientName
        self._running = True
        # Object that signals shutdown
        self._sentinel = 'SHUTDOWN'

    def terminate(self):
        self._running = False

    def run(self, n, started_event, stopped_event, out_q):
        self.flood('heart beat countdown started.')
        started_event.set()
        while self._running and n > 0:
            self.flood('heart beat countdown for ' + self.clientName + 'T-minus ' + str(n*5) + ' seconds.')
            n -= 1
            time.sleep(5)
        stopped_event.set()
        self.flood("heart beat countdown for " + self.clientName + " is shutting down.  stopped event = " + str(stopped_event.isSet()))
        # out_q.put(self._sentinel)

    def flood(self, message):
        print(message)
        self.log.info(message)
        self.sock.send(message + "\n")