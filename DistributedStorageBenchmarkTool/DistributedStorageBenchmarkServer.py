__author__ = 'shadoobie'
from SocketServer import ThreadingTCPServer
from DistributedStorageBenchmarkTool import EchoHandler
import logging

class DistributedStorageBenchmarkServer(ThreadingTCPServer):
    '''
    classdocs
    '''
    name = None
    log = None
    reportFileName = None


    def __init__(self, serverInfo, EchoHandler, log):
        '''
        Constructor
        '''
        self.name = "address-" + serverInfo[0] + "-port-" + str(serverInfo[1])
        self.log = log
        self.flood('DistributedStorageBenchmarkServer is being instantiated and initialized: ' + self.name)
        ThreadingTCPServer.__init__(self, serverInfo, EchoHandler)
        self.flood(self.name + ' is done initializing.')
        
        
    def getLogger(self):
        return self.log

    def flood(self, message):
        print(message)
        self.log.info(message)
