__author__ = 'python cookbook'
import time
import resource
from DistributedStorageBenchmarkTool.DataTask import DataTask
from threading import Thread, Event

class LaunchAndMeasureDataTask:
    def __init__(self, log, sock, clientName, chunkSize, maxFileSize, dataThreadName, countDownStoppedEvent):
        self._running = True
        self.name = 'report thread for client ' + clientName
        self.log = log
        self.sock = sock
        self.clientName = clientName
        self.chunkSize = chunkSize
        self.maxFileSize = maxFileSize
        self.dataThreadName = dataThreadName
        self.countDownStopEvent = countDownStoppedEvent
        self._sentinel = 'SHUTDOWN'
        self.dataTask = DataTask(self.log, self.sock, self.clientName, self.chunkSize, self.maxFileSize, self.countDownStopEvent)

    def terminate(self):
        self.dataTask.termiante()
        self._running = False

    def run(self, startedEvent, stoppedEvent, threadQueue):
        startedEvent.set()
        self.flood('report thread for ' + self.clientName + ' started. this thread launches the data thread and reports on its resource usage.')

        startedDataThreadEvent = Event()
        stoppedDataThreadEvent = Event()
        stopChildThreadEvent = Event()

        self.dataThread = Thread(name=self.dataThreadName, target=self.dataTask.run, args=(stopChildThreadEvent, startedDataThreadEvent, stoppedDataThreadEvent, threadQueue,))
        self.dataThread.start()
        # data = ''

        self.flood("++++++++++++   countDownStopEvent is_set = " + str(self.countDownStopEvent.isSet()))
        while self._running and not self.countDownStopEvent.isSet(): #self._sentinel not in data:
            self.flood("************   countDownStopEvent is_set = " + str(self.countDownStopEvent.isSet()))

            reportHeading = "==== 10 Second Resource Report On Child Processes ===="
            self.flood(reportHeading)
            usage = resource.getrusage(resource.RUSAGE_CHILDREN)
            self.flood('Report about to for loop')
            for name, desc in [
                ('ru_utime', 'User time'),
                ('ru_stime', 'System time'),
                ('ru_maxrss', 'Max. Resident Set Size'),
                ('ru_ixrss', 'Shared Memory Size'),
                ('ru_idrss', 'Unshared Memory Size'),
                ('ru_isrss', 'Stack Size'),
                ('ru_inblock', 'Block inputs'),
                ('ru_oublock', 'Block outputs'),
                ]:
                reportMessage = self.name + ': ' + '%-25s (%-10s) = %s' % (desc, name, getattr(usage, name))
                self.flood(reportMessage)
            time.sleep(10)
            # data = threadQueue.get()
            # self.flood(self.name + ' threadQueue data = ' + data)

        '''put the sentinal back in the threadQueue so that its child data thread will get the message to stop'''
        # threadQueue.put(self._sentinel)

        self.flood(self.name + ' report thread is trying to stop. countdown stop event = ' + str(self.countDownStopEvent.isSet()))
        stopChildThreadEvent.set()
        self.flood(self.name + ' terminating the data task.')
        self.dataTask.terminate()
        stoppedEvent.set()


    def flood(self, message):
        print(message)
        self.log.info(message)
        self.sock.send(message)