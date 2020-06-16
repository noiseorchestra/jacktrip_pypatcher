import jack
import jacktrip_pypatcher as p

dry_run = True
jackClient = jack.Client('MadwortAutoPatcher')

all_jacktrip_receive_ports = jackClient.get_ports('.*receive.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for	receive_port in all_jacktrip_receive_ports:
	p.disconnect_all(jackClient, receive_port)

# add some new jacktrip connections
print("=== Creating new connections ===")
jacktrip_clients = list(map(lambda x: x.name.split(':')[0],jackClient.get_ports('.*receive_1')))
print("client count:", len(jacktrip_clients))
print('clients', jacktrip_clients)

for	client in jacktrip_clients:
	client_hostname = client.split(':')[0]
	# get a list of target ip addresses to send this receive port to
	# TODO: these are not send_targets, they are receives!
	receive_targets = list(filter(lambda x: not x.startswith(client_hostname), jacktrip_clients))
	print("client", client_hostname, "with receive_targets:", receive_targets)
	if len(receive_targets) == 1:
		print('Only two clients, duplicate it')
		channel_1_receive_addresses = receive_targets
		channel_2_receive_addresses = receive_targets
	else:
		channel_1_receive_addresses = receive_targets[:len(receive_targets)//2]
		channel_2_receive_addresses = receive_targets[len(receive_targets)//2:]

	print("Targets split into two lists: ", channel_1_receive_addresses, " : ", channel_2_receive_addresses)

	for receive_address in channel_1_receive_addresses:
		receive_port = receive_address + ':receive_1'
		send_port = client_hostname + ':send_1'
		print('connect chan1', receive_port, 'to', send_port)
		try:
			jackClient.connect(receive_port, send_port)
		except JackError as e:
			print('error making connection', e)
	for receive_address in channel_2_receive_addresses:
		receive_port = receive_address + ':receive_1'
		send_port = client_hostname + ':send_2'
		send_port_list = jackClient.get_ports(send_port)
		print('connect chan2', receive_port, 'to', send_port)
		# fixup for mono clients
		if(len(send_port_list) > 0):
			try:
				jackClient.connect(receive_port, send_port)
			except JackError as e:
				print('error making connection', e)
		else:
			send_port = client_hostname + ':send_1'
			try:
				jackClient.connect(receive_port, send_port)
			except JackError as e:
				print('error making connection', e)
