import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DistributedStorageBenchmarkTool.ReadLogWriteReport import ReadLogWriteReport

if __name__ == '__main__':
    test = ReadLogWriteReport()
    blah = test.execute()