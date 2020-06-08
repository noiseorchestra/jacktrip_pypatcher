import jack

client = jack.Client('MadwortAutoPatcher')

all_jacktrip_receive_ports = client.get_ports('.*receive.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
for	receive_port in all_jacktrip_receive_ports:
	print(receive_port.name)
	send_ports = client.get_all_connections(receive_port)
	for send_port in send_ports:
		print(send_port)
		client.disconnect(receive_port, send_port)
	
# add some new jacktrip connections
jacktrip_receive_1_ports = client.get_ports('.*receive_1')
all_jacktrip_send_ports = client.get_ports('.*send.*')
print("client count: ", len(jacktrip_receive_1_ports))
channel_1_receive_ports = jacktrip_receive_1_ports[:len(jacktrip_receive_1_ports)//2]
channel_2_receive_ports = jacktrip_receive_1_ports[len(jacktrip_receive_1_ports)//2:]

print(channel_1_receive_ports)
print(channel_2_receive_ports)

for receive_port in channel_1_receive_ports:
	this_client = receive_port.name.split(':')[0]
	for send_port in all_jacktrip_send_ports:
		# TODO: just do it with regexes?
		if send_port.name.startswith(this_client):
			continue
		if send_port.name.endswith('send_1'):
			print('connect ', receive_port, send_port)
			client.connect(receive_port, send_port)

for receive_port in channel_2_receive_ports:
	this_client = receive_port.name.split(':')[0]
	for send_port in all_jacktrip_send_ports:
		if send_port.name.startswith(this_client):
			continue
		if send_port.name.endswith('send_2'):
			print('connect ', receive_port, send_port)
			client.connect(receive_port, send_port)
