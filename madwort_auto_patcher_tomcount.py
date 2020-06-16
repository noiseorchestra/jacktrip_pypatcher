import jack
import os
import random
import jacktrip_pypatcher as p

dry_run = True
jackClient = jack.Client('MadwortAutoPatcher')

# number_of_voices = random.randint(1,5)
number_of_voices = 5

all_mpg123_ports = jackClient.get_ports('mpg123-.*')
all_ladspa_ports = jackClient.get_ports('slight-.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for	mpg123_port in all_mpg123_ports:
	p.disconnect_all(jackClient, mpg123_port)

for	ladspa_port in all_ladspa_ports:
	p.disconnect_all(jackClient, ladspa_port)

# add some new jacktrip connections
print("=== Creating new connections ===")
mpg123_ports_all = list(map(lambda x: x.name.split(':')[0],jackClient.get_ports('mpg123.*:1')))
random.shuffle(mpg123_ports_all)
mpg123_ports = mpg123_ports_all[0:number_of_voices]

if dry_run:
	mpg123_ports = ['mpg123-one', 'mpg123-two']

print("count count:", len(mpg123_ports))
print('counts', mpg123_ports)

jacktrip_clients = list(map(lambda x: x.name.split(':')[0],jackClient.get_ports('.*receive_1')))

if dry_run:
	jacktrip_clients = ['..ffff.192.168.0.1', '..ffff.192.168.0.2', '..ffff.192.168.0.3', '..ffff.192.168.0.4', '..ffff.192.168.0.5', '..ffff.192.168.0.6']
	jacktrip_clients = jacktrip_clients[0:2]

print("client count:", len(jacktrip_clients))
print('clients', jacktrip_clients)

# RUN THESE FIRST!
# tom@noiseaa1:~$ mpg123-jack --name mpg123-one --loop -1 tom-count-one.mp3
# etc
# tom@noiseaa1:~/ng-jackspa$ ./jackspa-cli -j slight-right -i '0:0:0:0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
# tom@noiseaa1:~/ng-jackspa$ ./jackspa-cli -j slight-left -i '0:0:0:-0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &

for	jacktrip_client in jacktrip_clients:
	print("---")
	print("JackTrip client", jacktrip_client)
	if len(mpg123_ports) < 1:
		os._exit(1)

	if len(mpg123_ports) == 1:
		p.connect_to_centre(jackClient, mpg123_ports[0], jacktrip_client, dry_run)

	if len(mpg123_ports) >= 2:
		p.connect_to_left(jackClient, mpg123_ports[0], jacktrip_client, dry_run)
		p.connect_to_right(jackClient, mpg123_ports[1], jacktrip_client, dry_run)

	if len(mpg123_ports) == 3:
		p.connect_to_centre(jackClient, mpg123_ports[2], jacktrip_client, dry_run)

	if len(mpg123_ports) >= 4:
		p.connect_to_soft_left(jackClient, mpg123_ports[2], jacktrip_client, dry_run)
		p.connect_to_soft_right(jackClient, mpg123_ports[3], jacktrip_client, dry_run)

	if len(mpg123_ports) == 5:
		p.connect_to_centre(jackClient, mpg123_ports[4], jacktrip_client, dry_run)

os._exit(0)
