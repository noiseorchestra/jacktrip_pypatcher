import jacktrip_pypatcher as jtp
import time
from watchgod import run_process

def foobar():
  while True:
    jtp.main()
    time.sleep(3600)

run_process('/var/tmp/jacktrip_pypatcher', foobar)
