__author__ = 'shadoobie'
from datetime import datetime
import logging

class StampyMcGetTheLog:

    stamp = None

    def __init__(self):
        self.stamp = str(datetime.now()).replace(':', '.').replace(' ', '_')

    def getStamp(self):
        return self.stamp

    def getLogger(self, name, logFileNameComponent):
        logFileName = self.stamp + logFileNameComponent
        logging.basicConfig(name=name, filename=logFileName,level=logging.DEBUG)
        l = logging.getLogger(name)

        return l