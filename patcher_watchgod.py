import jacktrip_pypatcher as jtp
import time
import sys
from watchgod import run_process


def foobar():
    while True:
        try:
            time.sleep(2)
            jtp.main()
            time.sleep(6000)
        except Exception as e:
            print("pypatcher could not start:", e)
            sys.exit("Exited because of pypatcher error")


run_process("/var/tmp/jacktrip_pypatcher", foobar)
