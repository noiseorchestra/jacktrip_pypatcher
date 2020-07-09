import jack

client = jack.Client('MadwortAutoPatcher')

all_jacktrip_receive_ports = client.get_ports('.*receive.*')
all_jacktrip_send_ports = client.get_ports('.*send.*')

# remove all existing jacktrip connections (hubserver autopatcher)
# TODO: only remove autopatched connections, not our own connections (HOW?)
print("=== Disconnecting existing connections ===")
for	receive_port in all_jacktrip_receive_ports:
	send_ports = jackClient.get_all_connections(receive_port)
	for send_port in send_ports:
		# Do not disconnect from jack_capture ports.
		# They do auto-reconnect, but we do not need to, and 
		# the disconnection is not reliable
		if send_port.name.startswith('jack_capture'):
			continue
		print('disconnect', receive_port.name, 'from', send_port.name)
		client.disconnect(receive_port, send_port)
	
# add some new jacktrip connections
print("=== Creating new connections ===")
# this should match hubserver autopatch mode 2
for receive_port in all_jacktrip_receive_ports:
	this_client = receive_port.name.split(':')[0]
	for send_port in all_jacktrip_send_ports:
		# comment out these two lines for hubserver patch mode 4
		if send_port.name.startswith(this_client):
			continue
		# only supports -n2 (two channels) for now
		if receive_port.name.endswith('1') and send_port.name.endswith('1'):
			print('connect ', receive_port, send_port)
			client.connect(receive_port, send_port)
		if receive_port.name.endswith('2') and send_port.name.endswith('2'):
			print('connect ', receive_port, send_port)
			client.connect(receive_port, send_port)
