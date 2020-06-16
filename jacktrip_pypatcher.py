# Helper functions for autopatching JackTrip hubserver clients

def disconnect_all(jack_client, my_port):
	"""disconnect everything from a port"""
	send_ports = jack_client.get_all_connections(my_port)
	for send_port in send_ports:
		# do not disconnect from jack_capture ports
		# they do auto-reconnect, but the disconnection is not reliable
		if send_port.name.startswith('jack_capture'):
			continue
		print('disconnect', my_port.name, 'from', send_port.name)
		jack_client.disconnect(my_port, send_port)

def connect_to_centre(jack_client, receive, send):
	"""connect pair of receive ports to the send ports, centre panned"""
	jack_client.connect(receive + ':1', send + ':send_1')
	jack_client.connect(receive + ':2', send + ':send_2')

def connect_to_left(jack_client, receive, send):
	"""connect pair of receive ports to the send ports, left panned"""
	jack_client.connect(receive + ':1', send + ':send_1')
	jack_client.connect(receive + ':2', send + ':send_1')

def connect_to_right(jack_client, receive, send):
	"""connect pair of receive ports to the send ports, right panned"""
	jack_client.connect(receive + ':1', send + ':send_2')
	jack_client.connect(receive + ':2', send + ':send_2')

def connect_to_soft_left(jack_client, receive, send):
	jack_client.connect(receive + ':1', 'slight-left:Input (Left)')
	jack_client.connect('slight-left:Output (Left)', send + ':send_1')

	jack_client.connect(receive + ':2', 'slight-left:Input (Right)')
	jack_client.connect('slight-left:Output (Right)', send + ':send_2')

def connect_to_soft_right(jack_client, receive, send):
	jack_client.connect(receive + ':1', 'slight-right:Input (Left)')
	jack_client.connect('slight-right:Output (Left)', send + ':send_1')

	jack_client.connect(receive + ':2', 'slight-right:Input (Right)')
	jack_client.connect('slight-right:Output (Right)', send + ':send_2')
