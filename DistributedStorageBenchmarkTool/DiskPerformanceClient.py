__author__ = 'shadoobie'
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Event
from Queue import Queue
from DistributedStorageBenchmarkTool.CountdownTask import CountdownTask
from DistributedStorageBenchmarkTool.LaunchAndMeasureDataTask import LaunchAndMeasureDataTask
from DistributedStorageBenchmarkTool.StampyMcGetTheLog import StampyMcGetTheLog

class DiskPerformanceClient(object):
    '''
    classdocs
    '''

    def __init__(self, clientName, serverInfo, lifeSpan, chunkSize, maxFileSize, log):
        '''
        Constructor
        '''
        self.name = clientName + '-' + StampyMcGetTheLog().getStamp()
        self.lifeSpan = lifeSpan
        self.serverInfo = serverInfo
        self.log = log
        self.sock = self.getSocketConnection(serverInfo)
        self.chunkSize = chunkSize
        self.maxFileSize = maxFileSize
        self.flood('clientName: ' + self.name + ' starting.')
        self.flood(self.name + ' lifeSpan: ' + str((self.lifeSpan*5)) + ' seconds.')
        self.flood(self.name + ' maxFileSize: ' + str(maxFileSize) + ' MB.')
        self.launchThreadRunStuff()



    def getAverageTimeBetweenWrites(self):
        return .5


    def launchThreadRunStuff(self):
        self.threadQueue = Queue()
        heartBeatThreadName = 'heartbeat thread for client ' + self.name
        startedCountdownEvent = Event()
        stoppedCountdownEvent = Event()

        reportThreadName = 'report thread for client ' + self.name
        startedLaunchAndMeasureDataEvent = Event()
        stoppedLaunchAndMeasureDataEvent = Event()
        dataThreadName = 'data thread for client ' + self.name + ' child of report thread named ' + reportThreadName
        lAndMDT = LaunchAndMeasureDataTask(self.log, self.sock, self.name, self.chunkSize, self.maxFileSize, dataThreadName, stoppedCountdownEvent)
        self.reportThread = Thread(name=reportThreadName, target=lAndMDT.run, args=(startedLaunchAndMeasureDataEvent, stoppedLaunchAndMeasureDataEvent, Queue,))
        self.reportThread.start()

        c = CountdownTask(self.log, self.sock, self.name)
        self.heartBeatThread = Thread(name=heartBeatThreadName, target=c.run, args=(self.lifeSpan,startedCountdownEvent, stoppedCountdownEvent, self.threadQueue))
        self.heartBeatThread.start()

    def getSocketConnection(self, serverInfo):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(serverInfo)
        return s

    def getCountDownThread(self, threadName):
        t = Thread(target=self.countdown(self.lifeSpan, threadName), args=(self.lifeSpan,threadName))
        return t

    def send(self, message):
        self.sock.send(message + "\n")

    def flood(self, message):
        print(message)
        self.log.info(message)
        self.send(message)

    def close(self):
        self.flood(self.name + ' is closing connection to server ' + self.serverInfo[0] + ':' + str(self.serverInfo[1]))
        self.sock.close()