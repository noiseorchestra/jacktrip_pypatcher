import jack
import os
import random
import jack_client_patching as p
import lounge_music
import subprocess
import time
import psutil

dry_run = True
jackClient = jack.Client('MadwortAutoPatcher')

# number_of_voices = random.randint(1,5)
number_of_voices = 5

hold_music_port = 'lounge-music'

all_jacktrip_receive_ports = jackClient.get_ports('.*receive.*')
all_left_ladspa_ports = jackClient.get_ports('left-.*')
all_right_ladspa_ports = jackClient.get_ports('right-.*')
darkice_prefix = 'darkice'
if dry_run:
  all_hold_music_ports = []

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for receive_port in all_jacktrip_receive_ports:
  p.disconnect_all(jackClient, receive_port)

for ladspa_port in all_left_ladspa_ports:
  p.disconnect_all(jackClient, ladspa_port)

for ladspa_port in all_right_ladspa_ports:
  p.disconnect_all(jackClient, ladspa_port)

for port in all_hold_music_ports:
  p.disconnect_all(jackClient, port)

# add some new jacktrip connections
print("=== Creating new connections ===")
jacktrip_clients = list(map(lambda x: x.name.split(':')[0],
                            jackClient.get_ports('.*receive_1')))
if dry_run:
  jacktrip_clients = ['..ffff.192.168.0.1', '..ffff.192.168.0.2',
                      '..ffff.192.168.0.3', '..ffff.192.168.0.4',
                      '..ffff.192.168.0.5', '..ffff.192.168.0.6']
  jacktrip_clients = jacktrip_clients[0:number_of_voices]

# hard-coded list of client ips that send stereo input
jacktrip_stereo = []

if dry_run:
  jacktrip_stereo = ['..ffff.192.168.0.1', '..ffff.192.168.0.6']

jacktrip_clients_stereo = list(map(lambda x: x in jacktrip_stereo, jacktrip_clients))

print("client count:", len(jacktrip_clients))
print('clients', jacktrip_clients)
print('clients (stereo)', jacktrip_clients_stereo)

print("=== Verify/start supporting software (ladspa, mpg123, darkice) ===")
if len(jacktrip_clients) < 2:
  lounge_music.start_the_music(jackClient, hold_music_port)
else:
  lounge_music.kill_the_music(jackClient, hold_music_port)

darkice_ports = list(map(lambda x: x.name.split(':')[0],
                            jackClient.get_ports(darkice_prefix + '.*:left')))

if dry_run:
  darkice_ports = ['darkice-10545']

if len(darkice_ports) == 0:
  print("Start darkice first, please")
  os._exit(1)

darkice_port = darkice_ports[0]
print("darkice port:", darkice_port)

print("=== Creating new connections ===")
if len(jacktrip_clients) < 1:
  print("-- darkice --")
  p.connect_mpg123_to_darkice(jackClient, hold_music_port, darkice_port, dry_run)
  os._exit(1)

if len(jacktrip_clients) == 1:
  # patch hold music to the one client
  p.connect_mpg123_to_centre(jackClient, hold_music_port, jacktrip_clients[0], dry_run)

  # also connect loopback
  p.connect_to_centre(jackClient, jacktrip_clients[0], jacktrip_clients[0], dry_run, jacktrip_clients_stereo[0])

  print("-- darkice --")
  p.connect_mpg123_to_darkice(jackClient, hold_music_port, darkice_port, dry_run)
  p.connect_darkice_to_centre(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])

if len(jacktrip_clients) == 2:
  soft_pan_and_loopback = False

  if soft_pan_and_loopback:
    ladspa_soft_left = 'left-65'
    ladspa_soft_right = 'right-65'
    p.connect_to_ladspa(jackClient, jacktrip_clients[0], ladspa_soft_left, dry_run, jacktrip_clients_stereo[0])
    p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_soft_right, dry_run, jacktrip_clients_stereo[1])

    # client 0 - loopback panned left
    p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_clients[0], dry_run, jacktrip_clients_stereo[0])
    # client 0 - client 1 panned right
    p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_clients[1], dry_run, jacktrip_clients_stereo[1])

    # client 1 - client 0 panned left
    p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_clients[0], dry_run, jacktrip_clients_stereo[0])
    # client 1 - loopback panned right
    p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_clients[1], dry_run, jacktrip_clients_stereo[1])

    print("-- darkice --")
    p.connect_darkice_from_ladspa(jackClient, ladspa_soft_left, darkice_port, dry_run)
    p.connect_darkice_from_ladspa(jackClient, ladspa_soft_right, darkice_port, dry_run)
  else:
    p.connect_to_centre(jackClient, jacktrip_clients[1], jacktrip_clients[0], dry_run, jacktrip_clients_stereo[1])
    p.connect_to_centre(jackClient, jacktrip_clients[0], jacktrip_clients[1], dry_run, jacktrip_clients_stereo[0])

    print("-- darkice --")
    p.connect_darkice_to_left(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])
    p.connect_darkice_to_right(jackClient, jacktrip_clients[1], darkice_port, dry_run, jacktrip_clients_stereo[1])

if len(jacktrip_clients) == 3 or len(jacktrip_clients) == 4:
  p.connect_to_left(jackClient, jacktrip_clients[1], jacktrip_clients[0], dry_run, jacktrip_clients_stereo[1])
  p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_clients[0], dry_run, jacktrip_clients_stereo[2])

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[1], dry_run, jacktrip_clients_stereo[0])
  p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_clients[1], dry_run, jacktrip_clients_stereo[2])

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[2], dry_run, jacktrip_clients_stereo[0])
  p.connect_to_right(jackClient, jacktrip_clients[1], jacktrip_clients[2], dry_run, jacktrip_clients_stereo[1])

if len(jacktrip_clients) == 3:
  print("-- darkice --")
  p.connect_darkice_to_left(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])
  p.connect_darkice_to_centre(jackClient, jacktrip_clients[1], darkice_port, dry_run, jacktrip_clients_stereo[1])
  p.connect_darkice_to_right(jackClient, jacktrip_clients[2], darkice_port, dry_run, jacktrip_clients_stereo[2])

if len(jacktrip_clients) == 4:
  # Nb. these are in addition to the above block!
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[0], dry_run, jacktrip_clients_stereo[3])
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[1], dry_run, jacktrip_clients_stereo[3])
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[2], dry_run, jacktrip_clients_stereo[3])

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[3], dry_run, jacktrip_clients_stereo[0])
  p.connect_to_right(jackClient, jacktrip_clients[1], jacktrip_clients[3], dry_run, jacktrip_clients_stereo[1])
  p.connect_to_centre(jackClient, jacktrip_clients[2], jacktrip_clients[3], dry_run, jacktrip_clients_stereo[2])

  print("-- darkice --")
  ladspa_soft_left = 'left-50'
  ladspa_soft_right = 'right-50'
  p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_soft_left, dry_run, jacktrip_clients_stereo[1])
  p.connect_to_ladspa(jackClient, jacktrip_clients[2], ladspa_soft_right, dry_run, jacktrip_clients_stereo[2])

  p.connect_darkice_to_left(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])
  p.connect_darkice_from_ladspa(jackClient, ladspa_soft_left, darkice_port, dry_run)
  p.connect_darkice_from_ladspa(jackClient, ladspa_soft_right, darkice_port, dry_run)
  p.connect_darkice_to_right(jackClient, jacktrip_clients[3], darkice_port, dry_run, jacktrip_clients_stereo[3])

if len(jacktrip_clients) == 5:
  # We want to only use a minimum number of LADSPA plugins, so pan everyone to the same places in 
  # every mix & miss out the loopbacks
  ladspa_soft_left = 'left-50'
  ladspa_soft_right = 'right-50'
  p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_soft_left, dry_run, jacktrip_clients_stereo[1])
  p.connect_to_ladspa(jackClient, jacktrip_clients[3], ladspa_soft_right, dry_run, jacktrip_clients_stereo[3])

  for  jacktrip_client in jacktrip_clients:
    print("-- jacktrip client:", jacktrip_client, '--')
    if jacktrip_clients[0] == jacktrip_client:
      p.connect_to_left(jackClient, jacktrip_clients[2], jacktrip_client, dry_run, jacktrip_clients_stereo[2])
    else:
      p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_client, dry_run, jacktrip_clients_stereo[0])
    if jacktrip_clients[1] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_client, dry_run)
    if (jacktrip_clients[2] != jacktrip_client and
        jacktrip_clients[0] != jacktrip_client and
        jacktrip_clients[4] != jacktrip_client):
      p.connect_to_centre(jackClient, jacktrip_clients[2], jacktrip_client, dry_run, jacktrip_clients_stereo[2])
    if jacktrip_clients[3] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_client, dry_run)
    if jacktrip_clients[4] == jacktrip_client:
      p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_client, dry_run, jacktrip_clients_stereo[2])
    else:
      p.connect_to_right(jackClient, jacktrip_clients[4], jacktrip_client, dry_run, jacktrip_clients_stereo[4])

  print("-- darkice --")
  p.connect_darkice_to_left(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])
  p.connect_darkice_from_ladspa(jackClient, ladspa_soft_left, darkice_port, dry_run)
  p.connect_darkice_to_centre(jackClient, jacktrip_clients[2], darkice_port, dry_run, jacktrip_clients_stereo[2])
  p.connect_darkice_from_ladspa(jackClient, ladspa_soft_right, darkice_port, dry_run)
  p.connect_darkice_to_right(jackClient, jacktrip_clients[4], darkice_port, dry_run, jacktrip_clients_stereo[4])

if len(jacktrip_clients) == 6:
  # We want to only use a minimum number of LADSPA plugins, so pan everyone 
  # to the same places in every mix & miss out the loopbacks
  ladspa_left_1 = 'left-65'
  ladspa_left_2 = 'left-30'
  ladspa_right_1 = 'right-30'
  ladspa_right_2 = 'right-65'
  p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_left_1, dry_run, jacktrip_clients_stereo[1])
  p.connect_to_ladspa(jackClient, jacktrip_clients[2], ladspa_left_2, dry_run, jacktrip_clients_stereo[2])
  p.connect_to_ladspa(jackClient, jacktrip_clients[3], ladspa_right_1, dry_run, jacktrip_clients_stereo[3])
  p.connect_to_ladspa(jackClient, jacktrip_clients[4], ladspa_right_2, dry_run, jacktrip_clients_stereo[4])

  for jacktrip_client in jacktrip_clients:
    print("-- jacktrip client:", jacktrip_client, '--')
    if jacktrip_clients[0] != jacktrip_client:
      p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_client, dry_run, jacktrip_clients_stereo[0])
    if jacktrip_clients[1] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_left_1, jacktrip_client, dry_run)
    if jacktrip_clients[2] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_left_2, jacktrip_client, dry_run)
    if jacktrip_clients[3] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_right_1, jacktrip_client, dry_run)
    if jacktrip_clients[4] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_right_2, jacktrip_client, dry_run)
    if jacktrip_clients[5] != jacktrip_client:
      p.connect_to_right(jackClient, jacktrip_clients[5], jacktrip_client, dry_run, jacktrip_clients_stereo[5])

  print("-- darkice --")
  p.connect_darkice_to_left(jackClient, jacktrip_clients[0], darkice_port, dry_run, jacktrip_clients_stereo[0])
  p.connect_darkice_from_ladspa(jackClient, ladspa_left_1, darkice_port, dry_run)
  p.connect_darkice_from_ladspa(jackClient, ladspa_left_2, darkice_port, dry_run)
  p.connect_darkice_from_ladspa(jackClient, ladspa_right_1, darkice_port, dry_run)
  p.connect_darkice_from_ladspa(jackClient, ladspa_right_2, darkice_port, dry_run)
  p.connect_darkice_to_right(jackClient, jacktrip_clients[5], darkice_port, dry_run, jacktrip_clients_stereo[5])

if len(jacktrip_clients) >= 7:
  print("Not yet implemented")
  # 0 -> -1
  # n-1 -> 1
  # if n is odd, (n-1)/2 -> 0 (exact middle)
  #   also do the fixup that n=5 does to put middle->left/right in the monitor mixes
  # otherwise n*(200/(n-1))
  # Nb. this should work for 5+
  os._exit(1)

os._exit(0)
