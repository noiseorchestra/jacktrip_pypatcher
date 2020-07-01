# Helper functions for the lounge music

import jack
import subprocess
import time

def start_the_music(jackClient, port, debug = False):
  """start looping the hold music, if it isn't already playing"""
  all_hold_music_ports = jackClient.get_ports(port + '.*')

  if len(all_hold_music_ports) > 0:
    if debug:
      print("Lounge music already playing!")
    return

  if debug:
    print("Start the lounge music please!")

  hold_music_proc = subprocess.Popen(["mpg123-jack", "--name", port,
    "--no-control","-q","--loop","-1","/home/tom/lounge-music.mp3"])
  # wait for the jack client to register
  time.sleep(0.1)

  if debug:
    all_hold_music_ports = jackClient.get_ports(port + '.*')
    print(len(all_hold_music_ports))
