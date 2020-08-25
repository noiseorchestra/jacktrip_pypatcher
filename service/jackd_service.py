import sys
from subprocess import Popen, PIPE

try:
    command = ['jackd', '-R', '-dalsa', '-r48000', '-p256', '-n2', '-s', '-S']
    jack_process = Popen(command, stdout=PIPE, stderr=PIPE)
    # print output somehow
except Exception as e:
    print("JACK server didn't start:", e)
    sys.exit("JACK service exited because JACK server didn't start")
