__author__ = 'shadoobie'
import getopt, sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DistributedStorageBenchmarkTool.EchoHandler import EchoHandler
from DistributedStorageBenchmarkTool.DistributedStorageBenchmarkServer import DistributedStorageBenchmarkServer
from DistributedStorageBenchmarkTool.StampyMcGetTheLog import StampyMcGetTheLog

def main(argv):
    print("inside the main() method.")
    try:
        opts, args = getopt.getopt(argv, "h:o:a:p:", ["help", "output=", "address=", "port="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    output = '-BenchmarkTestServer.log'
    address = 'localhost'
    port = 24000

    for o, a in opts:
        # print('o = ' + o)
        # print('a = ' + a)
        if o in ("-a", "--address"):
            address = a
        elif o in ("-p", "--port"):
            portStr = a
            port = int(portStr)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print("output file =" + output)
        else:
            assert False, "unhandled option"
    # ...
    # start the DistributedStorageBenchmarkServer using the parameters passed to this script.

    log = StampyMcGetTheLog().getLogger('Server', output)
    server_info = (address, port)
    floodComms("Starting DistributedStorageBenchmarkServer on %s and port %s " % server_info, log)
    server = DistributedStorageBenchmarkServer(server_info, EchoHandler, log)
    floodComms("To stop the server either manually close the client connections, or wait for all connected clients to expire, then press ctrl-c.", log)
    try:
        server.serve_forever(0.5)
    except KeyboardInterrupt:
        floodComms("DistributedStorageBenchmarkServer detected ctrl-c keyboard interrupt. Attempting to exit gracefully.",log)
        server.shutdown()
        server.server_close()
        pass
    finally:
        floodComms("DistributedStorageBenchmarkServer at %s port %s has, I think, exited gracefully." % server_info, log)

def usage():
    print("This program starts a DistributedStorageBenchmarkServer for use with the TestDiskPerformance script.")

    print("-h or --help    : prints this help info.")
    print("-a or --address : specify the IP address or name of the computer running this test. The default is localhost")
    print("-p or --port    : specify the port to run the server on, the default is 24000")
    print("-o or --output  : specify part of the file name used to store the log for this test run. The default is -BenchmarkTestServer.log")
    print("Note that the log file will be prefixed with a time date stamp that sorts in chronological order on the OS.")

def floodComms(message, log):
    print(message)
    log.info(message)

if __name__ == "__main__":

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    finally:
        print("complete.")