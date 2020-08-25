import sys
from time import sleep
from subprocess import Popen, PIPE

try:
    command = ['jackd', '-R', '-dalsa', '-r48000', '-p256', '-n2', '-s', '-S']
    jack_process = Popen(command, stdout=PIPE, stderr=PIPE)
    while True:
        print(jack_process.stdout)
        sleep(0.1)
    # print output somehow
except Exception as e:
    print("JACK server didn't start:", e)
    sys.exit("JACK service exited because JACK server didn't start")
