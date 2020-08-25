import sys
from time import sleep
from subprocess import Popen, PIPE

try:
    command = ['mpg123-jack', '--name', 'lounge-music', '--loop', '-1', '~/lounge-music.mp3']
    mpg123_process = Popen(command, stdout=PIPE, stderr=PIPE)
    while True:
        print(mpg123_process.stdout.readline().rstrip(), 'utf-8'))
        sleep(0.1)
    # print output somehow
except Exception as e:
    print("mpg123-jack didn't start:", e)
    sys.exit("pypatcher service exited because mpg123-jack didn't start")
