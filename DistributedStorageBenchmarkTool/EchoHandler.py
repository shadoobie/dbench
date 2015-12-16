from SocketServer import BaseRequestHandler, TCPServer
from DistributedStorageBenchmarkTool.StampyMcGetTheLog import StampyMcGetTheLog
# from sets import Set
import re

class EchoHandler(BaseRequestHandler):

    name = None
    server = None
    chunkSizeWriteTimes = []
    chunkSizeSet = set()


    def __init__(self, request, client_address, server):
        self.server = server
        self.name = "EchoHandlerFor client " + str(client_address)
        self.server.flood("EchoHandler names " + self.name + " has been instantiated.")
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.server.flood(self.name + " handle() invoked.")
        while True:
            receivedData = self.request.recv(8192)
            self.server.flood("EchoHandler " + self.name + " receivedData = " + str(receivedData))
            if not receivedData: break
            self.request.sendall(receivedData)
        self.request.close()
        self.server.flood(self.name + " handel() has completed.")


    def lookForStuff(self, parsedData):
        '''this whole lookForStuff approach is wrong.  please forgive me for the code the ensues.  i did it wrong.'''
        lifeSpan = self.getLifeSpan(parsedData)
        maxFileSizeString = self.getMaxFileSizeString(parsedData)
        self.gatherChunkSizeAndWriteTimeMessages(parsedData)
        if lifeSpan != None and maxFileSizeString != None:
            maxFileSize = int(maxFileSizeString)
            for aChunkSize in self.chunkSizeSet:
                self.evaluateForRolloverCompliant(lifeSpan, maxFileSize, aChunkSize)

    def getClientName(self, parsedData):
        clientName = None
        if "clientName:" in parsedData:
            clientName = parsedData[1]

        return clientName

    def getLifeSpan(self, parsedData):
        lifeSpan = None
        if "lifeSpan:" in parsedData:
            lifeSpan = parsedData[2]
        else:
            lifeSpan = self.lifeSpan

        return lifeSpan

    def getMaxFileSizeString(self, parsedData):
        maxFileSize = None
        if "maxFileSize:" in parsedData:
            maxFileSize = parsedData[9]

        return maxFileSize

    def gatherChunkSizeAndWriteTimeMessages(self, parsedData):
        if "writeTime:" in parsedData:
            self.chunkSizeWriteTimes.append({'chunkSize':int(parsedData[3]), 'writeTime':float(parsedData[1])})
            self.chunkSizeSet.add(int(parsedData[3]))

    def getAverageTimeBetweenWritesForChunkSize(self, chunkSize):
        '''the first draft of this method probably not correct.'''
        average = sum(d['writeTime'] for d in self.chunkSizeWriteTimes) / len(self.chunkSizeWriteTimes)

        return average

    def evaluateForRolloverCompliant(self, lifeSpan, maxFileSize, chunkSize):

        numberOfSecondsRunning = lifeSpan
        howManySecondsBetweenEachChunkWrite = self.getAverageTimeBetweenWritesForChunkSize(chunkSize)

        numberOfChunksPerFile = maxFileSize / chunkSize
        numberOfSecondsPerFile = howManySecondsBetweenEachChunkWrite * numberOfChunksPerFile
        estimatedTotalFiles = numberOfSecondsRunning / numberOfSecondsPerFile

        if estimatedTotalFiles <= 2:
            self.server.flood(self.name + " says hey there I'm complaining that this test run will only roll over the data file an estimated " +
                                str(estimatedTotalFiles) + " number of files.")
        else:
            self.server.flood(self.name + " says it looks like we will have an estimated number of data files = " + str(estimatedTotalFiles))

    def parseLine(self,line):
        '''leverage regular expression to parse on space.'''
        parsedLine = re.split(r'\s',line)

        return parsedLine

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()