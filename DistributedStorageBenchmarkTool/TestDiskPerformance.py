__author__ = 'shadoobie'
import getopt, sys
import logging
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DistributedStorageBenchmarkTool.DiskPerformanceClient import DiskPerformanceClient
from DistributedStorageBenchmarkTool.StampyMcGetTheLog import StampyMcGetTheLog

def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:o:a:p:s:t:", ["help=", "output=", "address=", "port=", "filesize=", "time="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized" or that your -h or --help option requires an argument (sorry).
        usage()
        sys.exit(2)
    output = '-TestDiskPerformance.log'
    address = 'localhost'
    port = 24000
    chunkSizes = [1, 10, 50, 150]
    fileSize = 250
    time = 40

    for o, a in opts:
        if o in ("-a", "-address"):
            address = a
        elif o in ("-p", "-port"):
            portStr = a
            port = int(portStr)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print("output file =" + output)
        elif o in ("-s", "--filesize"):
            fileSize = int(a)
            print("filesize =" + output)
        elif o in ("-t", "--time"):
            time = int(a)
            print("time = " + str(time*5))
        else:
            assert False, "unhandled option"
    # ...
    log = StampyMcGetTheLog().getLogger('TestClients', output)
    server_info = (address, port)
    flood('Running TestDiskPerformance against server = ' + server_info[0] + " port = " + str(server_info[1]), log)
    dictionaryOfClients = {}
    n = 0
    for chunkSize in chunkSizes:
        clientName = "client" + str(n)
        if chunkSize >= 9:
            client = DiskPerformanceClient(clientName, server_info, time, chunkSize, fileSize, log)
            client.send(clientName + " instantiated.")
            dictionaryOfClients[clientName] = client
            n += 1
        else:
            print("Chunk size " + str(chunkSize) + " is too small, must be minimum of 10 MB. Skipping to the next chunk size in list.")
            log.error("Chunk size " + str(chunkSize) + " is too small, must be minimum of 10 MB. Skipping to the next chunk size in list.")

def usage():
    print("Instructions for the TestDiskPerformance script:")
    print("This program runs the TestDiskPerformance script. It requires that a DistributedStorageBenchmarchServer is running.")
    print("Use the StartBenchmarkTestServer script to start the DistributedStorageBenchmarchServer prior to running this test script.")
    print("Currently the chunk sizes are 10MB 100MB and 250MB. This file needs to be edited to add change or remove chunk size scenarios.")
    print("-h or --help     : prints this help info.")
    print("-a or --address  : specify the IP address or name of the computer running this test. The default is localhost")
    print("-p or --port     : specify the port to run the server on, the default is 24000")
    print("-s or --filesize : specify the size in MB of the data file used in performance testing. The default is 250 MB.")
    print("-t or --time     : specify the number of 5 second intervals the test will be constrained to (number of seconds times 5).")


def flood(message, log):
    print(message)
    log.info(message)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    except Exception:
        flood("===== There was an exception of some kind oh no! =====")
        message = Exception.message
        flood(Exception.message)
    finally:
        print("complete")
