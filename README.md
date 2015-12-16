# dbench

Possibly one of the most over used program names on the Internet.
This one is a distributed storage benchmark tool.

This tool measures and reports on how long it takes to write configurable chunks of data 
onto a set of distributed storage systems.  However currently there is no report, only a
log file or two (one for the server, and one for each client).

Python 2.7 is required and currently only works on modern Linux or OS/X operating systems.

<b>Happy Path Instructions:</b>

1. Unzip the dbench archive to the server computer and to each of the clients.
2. Have Python 2.7 installed such that you can run it from the command line (OS/X and Linux only).
3. From the server open a command line terminal to /dbench-master/DistributedStorageBenchmarkTool/ 
and issue the following command: <code>python StartBenchmarkTestServer.py -a server.name.or.ip</code>
4. From the client open a command line terminal to /dbench-master/DistributedStorageBenchmarkTool/ 
and issue the following command: <code>python TestDiskPerformance.py -a server.name.or.ip</code>

The tool's prototypical behavior is to write chunks of data to a file until the max file 
size has been reached then roll over.  This all happens for a period of time.  The clients 
send messages to the server and the client log and the server writes most everything to 
its own log too.  Most everything but the chunk sizes are configurable via the command line.
Use -h to see the settings.  The only setting that has really been tested is -a so good
luck!  

FYI - when the threads stop some of the requests encounter broken pipes as the test
winds down so among many other issues, that has to be looked at.

<pre>
python StartBenchmarkTestServer.py -h
inside the main() method.
option -h requires argument
This program starts a DistributedStorageBenchmarkServer for use with the TestDiskPerformance script.
-h or --help    : prints this help info.
-a or --address : specify the IP address or name of the computer running this test. The default is localhost
-p or --port    : specify the port to run the server on, the default is 24000
-o or --output  : specify part of the file name used to store the log for this test run. The default is -BenchmarkTestServer.log
Note that the log file will be prefixed with a time date stamp that sorts in chronological order on the OS.
complete.

python TestDiskPerformance.py -h
option -h requires argument
Instructions for the TestDiskPerformance script:
This program runs the TestDiskPerformance script. It requires that a DistributedStorageBenchmarchServer is running.
Use the StartBenchmarkTestServer script to start the DistributedStorageBenchmarchServer prior to running this test script.
Currently the chunk sizes are 10MB 100MB and 250MB. This file needs to be edited to add change or remove chunk size scenarios.
-h or --help     : prints this help info.
-a or --address  : specify the IP address or name of the computer running this test. The default is localhost
-p or --port     : specify the port to run the server on, the default is 24000
-s or --filesize : specify the size in MB of the data file used in performance testing. The default is 250 MB.
-t or --time     : specify the number of 5 second intervals the test will be constrained to (number of seconds times 5).
complete
</pre>

