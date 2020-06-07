import jack

client = jack.Client('MadwortAutoPatcher')

all_jacktrip_send_ports = client.get_ports('.*send.*')
all_jacktrip_receive_ports = client.get_ports('.*receive.*')

# remove all existing jacktrip connections (hubserver autopatcher)
for	receive_port in all_jacktrip_receive_ports:
	print(receive_port)
	send_ports = client.get_all_connections(receive_port)
	for send_port in send_ports:
		print(send_port)
		client.disconnect(receive_port, send_port)
	
# add some new jacktrip connections

