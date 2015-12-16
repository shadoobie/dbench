import re

class ReadLogWriteReport(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def execute(self):
        logFileName = 'log.txt'
        totals = self.getTotalDroppedPacketsByIp(logFileName)
        self.writeDroppedPacketsReport(totals)


    def parseLine(self,line):
        '''leverage regular expression to parse on space.'''
        parsedLine = re.split(r'\s',line)
        
        return parsedLine
        
        
    def getIpAddress(self, line):
        '''the line must be parsed for this method to work!'''
        ip = line[2]
        
        return ip
                
    def getMessage(self, line):
        '''the line must be parsed for this method to work!'''
        message = line[3]
        
        return message
    
    def getNumberOfDroppedPackets(self, line):
        numOfDroppedPackets = line[4]
        
        return numOfDroppedPackets
        
    def getTotalDroppedPacketsByIp(self, logFileName):
        totalsByIp = {}
        with open(logFileName, 'rt') as log:
            for line in log:
                parsedLine = self.parseLine(line)
                ip = self.getIpAddress(parsedLine)
                message = self.getMessage(parsedLine)
                if message in 'drops':
                    value = self.getNumberOfDroppedPackets(parsedLine)
                    existingValue = totalsByIp.get(ip)
                    if existingValue is None:
                        totalsByIp[ip] = int(value)
                    else:
                        totalsByIp[ip] = existingValue + int(value)
                                        
        return totalsByIp

    def writeDroppedPacketsReport(self, totals):        
        with open('report.txt', 'wt') as f:
            for key in totals.keys():
                ip = key
                totalPackets = totals[key]
                line = ip + ' drops total ' + str(totalPackets) + ' packets.\n'
                f.write(line)
            f.close()
