__author__ = 'shadoobie'

import os
from DistributedStorageBenchmarkTool.StampyMcGetTheLog import StampyMcGetTheLog
from DistributedStorageBenchmarkTool.Timer import Timer

class DataTask:
    def __init__(self, log, sock, clientName, chunkSize, maxFileSize, stopCountdownEvent):
        self._running = True
        self.log = log
        self.sock = sock
        self.clientName = clientName
        self.name = 'data thread for client ' + clientName
        self.chunkSize = chunkSize
        self.maxFileSize = maxFileSize
        self._running = True
        self._sentinel = 'SHUTDOWN'
        self.stopCountdownEvent = stopCountdownEvent
        self.stamp = StampyMcGetTheLog().getStamp()

    def terminate(self):
        self._running = False

    def generateChunk(self):
        chunkOData = 'X' * ((self.chunkSize * 1024) * 1024)

        return chunkOData

    def getDataFileName(self, number):
        fileName = self.stamp + '-data-file-' + str(number) + ".txt"
        return fileName

    def convertKiloBytesToMegaBytes(self, input_kilobyte):
        megabyte = float(0.000976562)
        convert_mb = megabyte * input_kilobyte
        return convert_mb

    def run(self, stopChildEvent, startedEvent, stoppedEvent, threadQueue):
        self.flood('DataTask started.')
        startedEvent.set()
        # data = ''
        n = 0
        fileName = self.getDataFileName(n)

        while self._running and not stopChildEvent.isSet() and not self.stopCountdownEvent.isSet(): # self._sentinel not in data:
            self.flood(self.name + ": writing chunks to a file:")
            self.flood(self.name  + " chunk size " + str(self.chunkSize) + "MB and max file size " + str(self.maxFileSize) + "MB")
            # data = threadQueue.get()
            # self.flood(self.name + ' threadQueue data = ' + data)

            fh = open(fileName,"wb")

            chunkOData = self.generateChunk()
            t = Timer()
            t.start()
            fh.write(chunkOData)
            t.stop()
            self.flood('writeTime: '+ str(t.elapsed) + " chunkSize: " + str(self.chunkSize) + " MB")
            fileSize = os.path.getsize(fileName)
            self.flood(self.name + " says the file size is " + str(fileSize) + " Bytes")
            fileSizeKBMaybe = fileSize / 1024
            self.flood(self.name + " says the file size is ~" + str(fileSizeKBMaybe) + " KB")
            if self.convertKiloBytesToMegaBytes(fileSizeKBMaybe) >= self.maxFileSize:
                fh.close()
                n += 1
                oldFileName = fileName
                fileName = self.getDataFileName(n)
                self.flood(self.name + " says that the data file is rolling over from " + oldFileName + " to " + fileName)

        # threadQueue.put(self._sentinel)

        self.flood("data thread " + self.name + " stopping.")
        stoppedEvent.set()



    def flood(self, message):
        print(message)
        self.log.info(message)
        self.sock.send(message)