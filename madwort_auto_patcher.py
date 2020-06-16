import jack
import os
import random
import jacktrip_pypatcher as p

dry_run = False
jackClient = jack.Client('MadwortAutoPatcher')

# number_of_voices = random.randint(1,5)
number_of_voices = 5

all_jacktrip_receive_ports = jackClient.get_ports('.*receive.*')
all_left_ladspa_ports = jackClient.get_ports('left-.*')
all_right_ladspa_ports = jackClient.get_ports('right-.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for receive_port in all_jacktrip_receive_ports:
  p.disconnect_all(jackClient, receive_port)

for ladspa_port in all_left_ladspa_ports:
  p.disconnect_all(jackClient, ladspa_port)

for ladspa_port in all_right_ladspa_ports:
  p.disconnect_all(jackClient, ladspa_port)

# add some new jacktrip connections
print("=== Creating new connections ===")
jacktrip_clients = list(map(lambda x: x.name.split(':')[0],
                            jackClient.get_ports('.*receive_1')))

if dry_run:
  jacktrip_clients = ['..ffff.192.168.0.1', '..ffff.192.168.0.2',
                      '..ffff.192.168.0.3', '..ffff.192.168.0.4',
                      '..ffff.192.168.0.5', '..ffff.192.168.0.6']
  jacktrip_clients = jacktrip_clients[0:2]

print("client count:", len(jacktrip_clients))
print('clients', jacktrip_clients)

# TODO: get this working
hold_music_port = 'lounge-music'

# RUN THESE FIRST!
# tom@noiseaa1:~$ mpg123-jack --name lounge-music --loop -1 ~tom/lounge-music.mp3

# TODO: Verify that the LADSPA plugins are running!

if len(jacktrip_clients) < 1:
  os._exit(1)

if len(jacktrip_clients) == 1:
  # patch hold music to the one client
  p.connect_to_centre(jackClient, hold_music_port, jacktrip_clients[0], dry_run)

if len(jacktrip_clients) == 2:
  soft_pan_and_loopback = True

  if soft_pan_and_loopback:
    ladspa_soft_left = 'left-65'
    ladspa_soft_right = 'right-65'
    p.connect_to_ladspa(jackClient, jacktrip_clients[0], ladspa_soft_left, dry_run)
    p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_soft_right, dry_run)

    # client 0 - loopback panned left
    p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_clients[0], dry_run)
    # client 0 - client 1 panned right
    p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_clients[1], dry_run)

    # client 1 - client 0 panned left
    p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_clients[0], dry_run)
    # client 1 - loopback panned right
    p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_clients[1], dry_run)
  else:
    p.connect_to_centre(jackClient, jacktrip_clients[1], jacktrip_clients[0], dry_run)
    p.connect_to_centre(jackClient, jacktrip_clients[0], jacktrip_clients[1], dry_run)

if len(jacktrip_clients) == 3 or len(jacktrip_clients) == 4:
  p.connect_to_left(jackClient, jacktrip_clients[1], jacktrip_clients[0], dry_run)
  p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_clients[0], dry_run)

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[1], dry_run)
  p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_clients[1], dry_run)

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[2], dry_run)
  p.connect_to_right(jackClient, jacktrip_clients[1], jacktrip_clients[2], dry_run)

if len(jacktrip_clients) == 4:
  # Nb. these are in addition to the above block!
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[0], dry_run)
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[1], dry_run)
  p.connect_to_centre(jackClient, jacktrip_clients[3], jacktrip_clients[2], dry_run)

  p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_clients[3], dry_run)
  p.connect_to_right(jackClient, jacktrip_clients[1], jacktrip_clients[3], dry_run)
  p.connect_to_centre(jackClient, jacktrip_clients[2], jacktrip_clients[3], dry_run)

if len(jacktrip_clients) == 5:
  # We want to only use a minimum number of LADSPA plugins, so do "missing 
  # person" style mixing - i.e. everyone is panned to the same places
  ladspa_soft_left = 'left-50'
  ladspa_soft_right = 'right-50'
  p.connect_to_ladspa(jackClient, jacktrip_clients[1], ladspa_soft_left, dry_run)
  p.connect_to_ladspa(jackClient, jacktrip_clients[3], ladspa_soft_right, dry_run)

  for  jacktrip_client in jacktrip_clients:
    print("-- jacktrip client:", jacktrip_client, '--')
    if jacktrip_clients[0] == jacktrip_client:
      p.connect_to_left(jackClient, jacktrip_clients[2], jacktrip_client, dry_run)
    else:
      p.connect_to_left(jackClient, jacktrip_clients[0], jacktrip_client, dry_run)
    if jacktrip_clients[1] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_soft_left, jacktrip_client, dry_run)
    if (jacktrip_clients[2] != jacktrip_client and
        jacktrip_clients[0] != jacktrip_client and
        jacktrip_clients[4] != jacktrip_client):
      p.connect_to_centre(jackClient, jacktrip_clients[2], jacktrip_client, dry_run)
    if jacktrip_clients[3] != jacktrip_client:
      p.connect_from_ladspa(jackClient, ladspa_soft_right, jacktrip_client, dry_run)
    if jacktrip_clients[4] == jacktrip_client:
      p.connect_to_right(jackClient, jacktrip_clients[2], jacktrip_client, dry_run)
    else:
      p.connect_to_right(jackClient, jacktrip_clients[4], jacktrip_client, dry_run)

if len(jacktrip_clients) >= 6:
  print("Not yet implemented")
  os._exit(1)

os._exit(0)
