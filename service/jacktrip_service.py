import sys
from time import sleep
from subprocess import Popen, PIPE

try:
    command = ['jacktrip', '-S', '-p0', '--nojackportsconnect']
    jacktrip_process = Popen(command, stdout=PIPE, stderr=PIPE)
    while True:
        print(jacktrip_process.stdout)
        sleep(0.1)
    # print output somehow
except Exception as e:
    print("JackTrip didn't start:", e)
    sys.exit("JackTrip service exited because JackTrip didn't start")
