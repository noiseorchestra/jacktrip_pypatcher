#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

try:
    command = ['python3', 'patcher_callback']
    callback_process = Popen(command, stdout=PIPE, stderr=PIPE)
    # print output somehow
except Exception as e:
    print("patcher_callback didn't start:", e)
    sys.exit("pypatcher service exited because patcher_callback didn't start")

try:
    command = ['python3', 'watchgod.py']
    watchgod_process = Popen(command, stdout=PIPE, stderr=PIPE)
    # print output somehow
except Exception as e:
    print("patcher_watchgod didn't start:", e)
    sys.exit("pypatcher service exited because patcher_watchgod didn't start")
