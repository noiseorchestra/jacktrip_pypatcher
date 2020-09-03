# Helper functions for the lounge music

import jack
import psutil
import subprocess
import time

def start_the_music(jackClient, port, debug = True):
  """start looping the hold music, if it isn't already playing"""
  hold_music_file_path = "/home/tom/lounge-music.mp3"

  all_hold_music_ports = jackClient.get_ports(port + '.*')

  if len(all_hold_music_ports) > 0:
    if debug:
      print("Lounge music already playing!")
    return

  if debug:
    print("Start the lounge music please!")

  # TODO: change to `mpg123.bin -o jack`
  hold_music_proc = subprocess.Popen(["mpg123-jack", "--name", port,
    "--no-control","-q","--loop","-1",hold_music_file_path])
  # wait for the jack client to register
  time.sleep(0.1)

  if debug:
    all_hold_music_ports = jackClient.get_ports(port + '.*')
    print(len(all_hold_music_ports))

def kill_the_music(jackClient, port, debug = True):
  """kill the hold music, if it's playing"""
  all_hold_music_ports = jackClient.get_ports(port + '.*')

  if len(all_hold_music_ports) == 0:
    if debug:
      print("Lounge music is not playing!")
    return

  if debug:
    print("Kill the lounge music please!")

  for proc in psutil.process_iter():
    if 'mpg123.bin' in proc.name():
      if port in proc.cmdline():
        print("Killing lounge music process id: ",proc.pid)
        proc.terminate()
        # proc.wait()
  time.sleep(0.1)

  if debug:
    all_hold_music_ports = jackClient.get_ports(port + '.*')
    print(len(all_hold_music_ports))
