import jack
import os
import random

jackClient = jack.Client('MadwortAutoPatcher')

# number_of_voices = random.randint(1,5)
number_of_voices = 5

def disconnect_all(my_port):
	"""disconnect everything from a port"""
	send_ports = jackClient.get_all_connections(my_port)
	for send_port in send_ports:
		# do not disconnect from jack_capture ports
		# they do auto-reconnect, but the disconnection is not reliable
		if send_port.name.startswith('jack_capture'):
			continue
		print('disconnect', my_port.name, 'from', send_port.name)
		jackClient.disconnect(my_port, send_port)

def connect_to_centre(receive, send):
	"""connect pair of receive ports to the send ports, centre panned"""
	jackClient.connect(receive + ':1', send + ':send_1')
	jackClient.connect(receive + ':2', send + ':send_2')

def connect_to_left(receive, send):
	"""connect pair of receive ports to the send ports, left panned"""
	jackClient.connect(receive + ':1', send + ':send_1')
	jackClient.connect(receive + ':2', send + ':send_1')

def connect_to_right(receive, send):
	"""connect pair of receive ports to the send ports, right panned"""
	jackClient.connect(receive + ':1', send + ':send_2')
	jackClient.connect(receive + ':2', send + ':send_2')

def connect_to_soft_left(receive, send):
	jackClient.connect(receive + ':1', 'slight-left:Input (Left)')
	jackClient.connect('slight-left:Output (Left)', send + ':send_1')

	jackClient.connect(receive + ':2', 'slight-left:Input (Right)')
	jackClient.connect('slight-left:Output (Right)', send + ':send_2')

def connect_to_soft_right(receive, send):
	jackClient.connect(receive + ':1', 'slight-right:Input (Left)')
	jackClient.connect('slight-right:Output (Left)', send + ':send_1')
	
	jackClient.connect(receive + ':2', 'slight-right:Input (Right)')
	jackClient.connect('slight-right:Output (Right)', send + ':send_2')


all_mpg123_ports = jackClient.get_ports('mpg123-.*')
all_ladspa_ports = jackClient.get_ports('slight-.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for	mpg123_port in all_mpg123_ports:
	disconnect_all(mpg123_port)

for	ladspa_port in all_ladspa_ports:
	disconnect_all(ladspa_port)

# add some new jacktrip connections
print("=== Creating new connections ===")
mpg123_ports_all = list(map(lambda x: x.name.split(':')[0],jackClient.get_ports('mpg123.*:1')))
random.shuffle(mpg123_ports_all)
mpg123_ports = mpg123_ports_all[0:number_of_voices]
print("count count:", len(mpg123_ports))
print('counts', mpg123_ports)

jacktrip_clients = list(map(lambda x: x.name.split(':')[0],jackClient.get_ports('.*receive_1')))
print("client count:", len(jacktrip_clients))
print('clients', jacktrip_clients)

# RUN THESE FIRST!
# tom@noiseaa1:~$ mpg123-jack --name mpg123-one --loop -1 tom-count-one.mp3
# etc
# tom@noiseaa1:~/ng-jackspa$ ./jackspa-cli -j slight-right -i '0:0:0:0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
# tom@noiseaa1:~/ng-jackspa$ ./jackspa-cli -j slight-left -i '0:0:0:-0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &

for	jacktrip_client in jacktrip_clients:
	if len(mpg123_ports) < 1:
		os._exit(1)

	if len(mpg123_ports) == 1:
		connect_to_centre(mpg123_ports[0], jacktrip_client)

	if len(mpg123_ports) >= 2:
		connect_to_left(mpg123_ports[0], jacktrip_client)
		connect_to_right(mpg123_ports[1], jacktrip_client)

	if len(mpg123_ports) == 3:
		connect_to_centre(mpg123_ports[2], jacktrip_client)

	if len(mpg123_ports) >= 4:
		connect_to_soft_left(mpg123_ports[2], jacktrip_client)
		connect_to_soft_right(mpg123_ports[3], jacktrip_client)

	if len(mpg123_ports) == 5:
		connect_to_centre(mpg123_ports[4], jacktrip_client)

os._exit(0)
