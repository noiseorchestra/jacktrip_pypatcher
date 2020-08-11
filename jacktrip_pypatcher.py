import jack
import os
import psutil
import random
import jack_client_patching as p

def disconnect(jackClient, dry_run, hold_music_port):
  """Disconnect all autopatched ports"""
  # TODO: only remove autopatched connections, not our own connections (HOW?)
  all_jacktrip_receive_ports = jackClient.get_ports('.*receive.*')
  all_left_ladspa_ports = jackClient.get_ports('left-.*')
  all_right_ladspa_ports = jackClient.get_ports('right-.*')
  all_hold_music_ports = jackClient.get_ports(hold_music_port + '.*')
  if dry_run:
    all_hold_music_ports = []

  jcp = p.JackClientPatching(jackClient, dry_run)

  # TODO: implement dry_run mode!
  for receive_port in all_jacktrip_receive_ports:
    jcp.disconnect_all(receive_port)

  for ladspa_port in all_left_ladspa_ports:
    jcp.disconnect_all(ladspa_port)

  for ladspa_port in all_right_ladspa_ports:
    jcp.disconnect_all(ladspa_port)

  for port in all_hold_music_ports:
    jcp.disconnect_all(port)

def get_current_clients(jackClient, dry_run):
  """Get an array of client jack port prefixes"""
  return list(map(lambda x: x.name.split(':')[0],
                              jackClient.get_ports('.*receive_1')))

def verify_ladspa_plugins(jackClient):
  """Verify that the LADSPA plugins are running and abort if not"""
  all_left_ladspa_ports = jackClient.get_ports('left-.*')
  if len(all_left_ladspa_ports) < 1:
    print("Start LADSPA plugins please!")
    # TODO: verify SystemExit is working as intended
    SystemExit(1)

def get_darkice_port(jackClient, dry_run, darkice_prefix):
  """Get the current darkice jack port prefix"""
  darkice_ports = list(map(lambda x: x.name.split(':')[0],
                              jackClient.get_ports(darkice_prefix + '.*:left')))

  if dry_run:
    darkice_ports = ['darkice-10545']

  if len(darkice_ports) == 0:
    print("Start darkice first, please")
    SystemExit(1)

  return darkice_ports[0]

# return process object of relevant jack_capture, if running
def darkice_recording_process():
  for proc in psutil.process_iter(['pid', 'name', 'username','cmdline']):
    if(proc.name() == 'jack_capture'):
      if(proc.cmdline()[2] == 'darkice-'):
        return proc
  return False

def start_darkice_recording():
  # run `jack_capture --filename-prefix darkice- -S --channels 2 --port darkice\*`
  return True

def stop_darkice_recording():
  myprocess = darkice_recording_process()
  if not myprocess:
    return True
  myprocess.kill()

def autopatch(jackClient, dry_run, jacktrip_clients, jacktrip_clients_stereo):
  """Autopatch all the things!"""

  print("=== Clients ===")
  print("client count:", len(jacktrip_clients))
  print('clients', jacktrip_clients)
  print('clients (stereo)', jacktrip_clients_stereo)

  # RUN THESE FIRST!
  # tom@noiseaa1:~$ mpg123-jack --name lounge-music --loop -1 ~tom/lounge-music.mp3
  hold_music_port = 'lounge-music'
  darkice_prefix = 'darkice'

  print("=== Disconnecting existing connections ===")
  disconnect(jackClient, dry_run, hold_music_port)

  # add some new jacktrip connections
  print("=== Creating new connections ===")

  if len(jacktrip_clients) > 3:
    verify_ladspa_plugins(jackClient)

  darkice_port = get_darkice_port(jackClient, dry_run, darkice_prefix)
  print("darkice port:", darkice_port)

  jcp = p.JackClientPatching(jackClient, dry_run)

  max_supported_clients = 11
  if len(jacktrip_clients) > max_supported_clients:
    print("Unsupported number of clients, patching", max_supported_clients, "of",
          len(jacktrip_clients))
    jacktrip_clients = jacktrip_clients[0:max_supported_clients]

  if len(jacktrip_clients) < 1:
    print("-- darkice --")
    jcp.connect_mpg123_to_darkice(hold_music_port, darkice_port)
    stop_darkice_recording()
    SystemExit(1)
  else:
    start_darkice_recording()

  if len(jacktrip_clients) == 1:
    # patch hold music to the one client
    jcp.connect_mpg123_to_centre(hold_music_port, jacktrip_clients[0])

    # also connect loopback
    jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[0], jacktrip_clients_stereo[0])

    print("-- darkice --")
    jcp.connect_mpg123_to_darkice(hold_music_port, darkice_port)
    jcp.connect_darkice_to_centre(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])

  if len(jacktrip_clients) == 2:
    soft_pan_and_loopback = False

    if soft_pan_and_loopback:
      ladspa_soft_left = 'left-65'
      ladspa_soft_right = 'right-65'
      jcp.connect_to_ladspa(jacktrip_clients[0], ladspa_soft_left, jacktrip_clients_stereo[0])
      jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_soft_right, jacktrip_clients_stereo[1])

      # client 0 - loopback panned left
      jcp.connect_from_ladspa(ladspa_soft_left, jacktrip_clients[0], jacktrip_clients_stereo[0])
      # client 0 - client 1 panned right
      jcp.connect_from_ladspa(ladspa_soft_left, jacktrip_clients[1], jacktrip_clients_stereo[1])

      # client 1 - client 0 panned left
      jcp.connect_from_ladspa(ladspa_soft_right, jacktrip_clients[0], jacktrip_clients_stereo[0])
      # client 1 - loopback panned right
      jcp.connect_from_ladspa(ladspa_soft_right, jacktrip_clients[1], jacktrip_clients_stereo[1])

      print("-- darkice --")
      jcp.connect_darkice_from_ladspa(ladspa_soft_left, darkice_port)
      jcp.connect_darkice_from_ladspa(ladspa_soft_right, darkice_port)
    else:
      jcp.connect_to_centre(jacktrip_clients[1], jacktrip_clients[0], jacktrip_clients_stereo[1])
      jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[1], jacktrip_clients_stereo[0])

      print("-- darkice --")
      jcp.connect_darkice_to_left(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])
      jcp.connect_darkice_to_right(jacktrip_clients[1], darkice_port, jacktrip_clients_stereo[1])

  if len(jacktrip_clients) == 3 or len(jacktrip_clients) == 4:
    jcp.connect_to_left(jacktrip_clients[1], jacktrip_clients[0], jacktrip_clients_stereo[1])
    jcp.connect_to_right(jacktrip_clients[2], jacktrip_clients[0], jacktrip_clients_stereo[2])

    jcp.connect_to_left(jacktrip_clients[0], jacktrip_clients[1], jacktrip_clients_stereo[0])
    jcp.connect_to_right(jacktrip_clients[2], jacktrip_clients[1], jacktrip_clients_stereo[2])

    jcp.connect_to_left(jacktrip_clients[0], jacktrip_clients[2], jacktrip_clients_stereo[0])
    jcp.connect_to_right(jacktrip_clients[1], jacktrip_clients[2], jacktrip_clients_stereo[1])

  if len(jacktrip_clients) == 3:
    print("-- darkice --")
    jcp.connect_darkice_to_left(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])
    jcp.connect_darkice_to_centre(jacktrip_clients[1], darkice_port, jacktrip_clients_stereo[1])
    jcp.connect_darkice_to_right(jacktrip_clients[2], darkice_port, jacktrip_clients_stereo[2])

  if len(jacktrip_clients) == 4:
    # Nb. these are in addition to the above block!
    jcp.connect_to_centre(jacktrip_clients[3], jacktrip_clients[0], jacktrip_clients_stereo[3])
    jcp.connect_to_centre(jacktrip_clients[3], jacktrip_clients[1], jacktrip_clients_stereo[3])
    jcp.connect_to_centre(jacktrip_clients[3], jacktrip_clients[2], jacktrip_clients_stereo[3])

    jcp.connect_to_left(jacktrip_clients[0], jacktrip_clients[3], jacktrip_clients_stereo[0])
    jcp.connect_to_right(jacktrip_clients[1], jacktrip_clients[3], jacktrip_clients_stereo[1])
    jcp.connect_to_centre(jacktrip_clients[2], jacktrip_clients[3], jacktrip_clients_stereo[2])

    print("-- darkice --")
    ladspa_soft_left = 'left-50'
    ladspa_soft_right = 'right-50'
    jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_soft_left, jacktrip_clients_stereo[1])
    jcp.connect_to_ladspa(jacktrip_clients[2], ladspa_soft_right, jacktrip_clients_stereo[2])

    jcp.connect_darkice_to_left(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])
    jcp.connect_darkice_from_ladspa(ladspa_soft_left, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_soft_right, darkice_port)
    jcp.connect_darkice_to_right(jacktrip_clients[3], darkice_port, jacktrip_clients_stereo[3])

  if len(jacktrip_clients) == 5:
    # We want to only use a minimum number of LADSPA plugins, so pan everyone to the same places in 
    # every mix & miss out the loopbacks
    ladspa_soft_left = 'left-50'
    ladspa_soft_right = 'right-50'
    jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_soft_left, jacktrip_clients_stereo[1])
    jcp.connect_to_ladspa(jacktrip_clients[3], ladspa_soft_right, jacktrip_clients_stereo[3])

    for  jacktrip_client in jacktrip_clients:
      print("-- jacktrip client:", jacktrip_client, '--')
      if jacktrip_clients[0] == jacktrip_client:
        jcp.connect_to_left(jacktrip_clients[2], jacktrip_client, jacktrip_clients_stereo[2])
      else:
        jcp.connect_to_left(jacktrip_clients[0], jacktrip_client, jacktrip_clients_stereo[0])
      if jacktrip_clients[1] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_soft_left, jacktrip_client)
      if (jacktrip_clients[2] != jacktrip_client and
          jacktrip_clients[0] != jacktrip_client and
          jacktrip_clients[4] != jacktrip_client):
        jcp.connect_to_centre(jacktrip_clients[2], jacktrip_client, jacktrip_clients_stereo[2])
      if jacktrip_clients[3] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_soft_right, jacktrip_client)
      if jacktrip_clients[4] == jacktrip_client:
        jcp.connect_to_right(jacktrip_clients[2], jacktrip_client, jacktrip_clients_stereo[2])
      else:
        jcp.connect_to_right(jacktrip_clients[4], jacktrip_client, jacktrip_clients_stereo[4])

    print("-- darkice --")
    jcp.connect_darkice_to_left(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])
    jcp.connect_darkice_from_ladspa(ladspa_soft_left, darkice_port)
    jcp.connect_darkice_to_centre(jacktrip_clients[2], darkice_port, jacktrip_clients_stereo[2])
    jcp.connect_darkice_from_ladspa(ladspa_soft_right, darkice_port)
    jcp.connect_darkice_to_right(jacktrip_clients[4], darkice_port, jacktrip_clients_stereo[4])

  if len(jacktrip_clients) > 5:
    ladspa_left_20 = 'left-20'
    ladspa_left_40 = 'left-40'
    ladspa_left_60 = 'left-60'
    ladspa_left_80 = 'left-80'
    ladspa_right_20 = 'right-20'
    ladspa_right_40 = 'right-40'
    ladspa_right_60 = 'right-60'
    ladspa_right_80 = 'right-80'

  if len(jacktrip_clients) >= 6:
    # We want to only use a minimum number of LADSPA plugins, so pan everyone to the same places in 
    # every mix & miss out the loopbacks
    jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_left_20, jacktrip_clients_stereo[1])
    jcp.connect_to_ladspa(jacktrip_clients[2], ladspa_right_20, jacktrip_clients_stereo[2])
    jcp.connect_to_ladspa(jacktrip_clients[3], ladspa_left_60, jacktrip_clients_stereo[3])
    jcp.connect_to_ladspa(jacktrip_clients[4], ladspa_right_60, jacktrip_clients_stereo[4])

    for jacktrip_client in jacktrip_clients:
      print("-- jacktrip client:", jacktrip_client, '--')
      if jacktrip_clients[0] != jacktrip_client:
        jcp.connect_to_left(jacktrip_clients[0], jacktrip_client, jacktrip_clients_stereo[0])
      if jacktrip_clients[1] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_left_20, jacktrip_client)
      if jacktrip_clients[2] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_right_20, jacktrip_client)
      if jacktrip_clients[3] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_left_60, jacktrip_client)
      if jacktrip_clients[4] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_right_60, jacktrip_client)
      if jacktrip_clients[5] != jacktrip_client:
        jcp.connect_to_right(jacktrip_clients[5], jacktrip_client, jacktrip_clients_stereo[5])

    print("-- darkice --")
    jcp.connect_darkice_to_left(jacktrip_clients[0], darkice_port, jacktrip_clients_stereo[0])
    jcp.connect_darkice_from_ladspa(ladspa_left_20, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_right_20, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_left_60, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_right_60, darkice_port)
    jcp.connect_darkice_to_right(jacktrip_clients[5], darkice_port, jacktrip_clients_stereo[5])

  if len(jacktrip_clients) >= 8:
    jcp.connect_to_ladspa(jacktrip_clients[6], ladspa_left_40, jacktrip_clients_stereo[6])
    jcp.connect_to_ladspa(jacktrip_clients[7], ladspa_right_40, jacktrip_clients_stereo[7])

    for jacktrip_client in jacktrip_clients:
      print("-- jacktrip client:", jacktrip_client, '--')
      if jacktrip_clients[6] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_left_40, jacktrip_client)
      if jacktrip_clients[7] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_right_40, jacktrip_client)

    print("-- darkice --")
    jcp.connect_darkice_from_ladspa(ladspa_left_40, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_right_40, darkice_port)

  if len(jacktrip_clients) >= 10:
    jcp.connect_to_ladspa(jacktrip_clients[8], ladspa_left_80, jacktrip_clients_stereo[8])
    jcp.connect_to_ladspa(jacktrip_clients[9], ladspa_right_80, jacktrip_clients_stereo[9])

    for jacktrip_client in jacktrip_clients:
      print("-- jacktrip client:", jacktrip_client, '--')
      if jacktrip_clients[8] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_left_80, jacktrip_client)
      if jacktrip_clients[9] != jacktrip_client:
        jcp.connect_from_ladspa(ladspa_right_80, jacktrip_client)

    print("-- darkice --")
    jcp.connect_darkice_from_ladspa(ladspa_left_80, darkice_port)
    jcp.connect_darkice_from_ladspa(ladspa_right_80, darkice_port)

  # Odd numbered client counts from 7-11
  if (len(jacktrip_clients) >= 6) and (len(jacktrip_clients)%2 == 1):
    last_client_index = len(jacktrip_clients)-1
    for jacktrip_client in jacktrip_clients:
      print("-- jacktrip client:", jacktrip_client, '--')
      if (jacktrip_clients[last_client_index] != jacktrip_client):
        jcp.connect_to_centre(jacktrip_clients[last_client_index], jacktrip_client, jacktrip_clients_stereo[last_client_index])
    print("-- darkice --")
    jcp.connect_darkice_to_centre(jacktrip_clients[last_client_index], darkice_port, jacktrip_clients_stereo[last_client_index])

  if len(jacktrip_clients) > 11:
    print("Not yet implemented")
    SystemExit(1)

  print("== Finished ==")

def main(dry_run = False):
  """Do some setup, then do the autopatch"""
  jackClient = jack.Client('MadwortAutoPatcher')

  jacktrip_clients = get_current_clients(jackClient, dry_run)

  # hard-coded list of client ips that send stereo input
  # TODO: move this to command-line option / config file
  jacktrip_stereo = []

  jacktrip_clients_stereo = list(map(lambda x: x in jacktrip_stereo, jacktrip_clients))

  return autopatch(jackClient, dry_run, jacktrip_clients, jacktrip_clients_stereo)

if __name__ == "__main__":
  main()
