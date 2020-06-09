import jack

client = jack.Client('MadwortAutoPatcher')

all_jacktrip_receive_ports = client.get_ports('.*receive.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for	receive_port in all_jacktrip_receive_ports:
	print(receive_port.name)
	send_ports = client.get_all_connections(receive_port)
	for send_port in send_ports:
		print(send_port.name)
		client.disconnect(receive_port, send_port)
	
# add some new jacktrip connections
print("=== Creating new connections ===")
jacktrip_receive_1_ports = client.get_ports('.*receive_1')
print("client count:", len(jacktrip_receive_1_ports))

for	receive_port in jacktrip_receive_1_ports:
	this_client = receive_port.name.split(':')[0]
	# get a list of target ip addresses to send this receive port to
	send_targets = list(map(lambda x: x.name.split(':')[0],filter(lambda x: not x.name.startswith(this_client),jacktrip_receive_1_ports)))
	print("client", this_client, "with send_targets:", send_targets)
	channel_1_send_addresses = send_targets[:len(send_targets)//2]
	channel_2_send_addresses = send_targets[len(send_targets)//2:]

	print("Targets split into two lists: ", channel_1_send_addresses, " : ", channel_2_send_addresses)

	for send_address in channel_1_send_addresses:
		send_port = send_address + ':send_1'
		print('connect chan1', receive_port.name, 'to', send_port)
		client.connect(receive_port.name, send_port)
	for send_address in channel_2_send_addresses:
		send_port = send_address + ':send_2'
		print('connect chan2', receive_port.name, 'to', send_port)
		client.connect(receive_port.name, send_port)
