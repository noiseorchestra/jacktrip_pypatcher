# Helper functions for autopatching JackTrip hubserver clients

def disconnect_all(jack_client, my_port, dry_run = False):
  """disconnect everything from a port"""
  send_ports = jack_client.get_all_connections(my_port)
  for send_port in send_ports:
    # do not disconnect from jack_capture ports
    # they do auto-reconnect, but the disconnection is not reliable
    if send_port.name.startswith('jack_capture'):
      continue
    print('disconnect', my_port.name, 'from', send_port.name)
    jack_client.disconnect(my_port, send_port)

def connect_to_centre(jack_client, receive, send, dry_run = False):
  """connect pair of receive ports to the send ports, centre panned"""
  if dry_run:
    print("Connect centre", receive, "to", send)
    return
  jack_client.connect(receive + ':receive_1', send + ':send_1')
  jack_client.connect(receive + ':receive_2', send + ':send_2')

def connect_mpg123_to_centre(jack_client, mpg123, send, dry_run = False):
  """connect an instance of mpg123-jack to a jacktrip client"""
  if dry_run:
    print("Connect mpg123 centre", mpg123, "to", send)
    return
  jack_client.connect(mpg123 + ':1', send + ':send_1')
  jack_client.connect(mpg123 + ':2', send + ':send_2')

def connect_to_left(jack_client, receive, send, dry_run = False):
  """connect pair of receive ports to the send ports, left panned"""
  if dry_run:
    print("Connect left", receive, "to", send)
    return
  jack_client.connect(receive + ':receive_1', send + ':send_1')
  jack_client.connect(receive + ':receive_2', send + ':send_1')

def connect_to_right(jack_client, receive, send, dry_run = False):
  """connect pair of receive ports to the send ports, right panned"""
  if dry_run:
    print("Connect right", receive, "to", send)
    return
  jack_client.connect(receive + ':receive_1', send + ':send_2')
  jack_client.connect(receive + ':receive_2', send + ':send_2')

def connect_to_ladspa(jack_client, receive, ladspa, dry_run = False):
  """connect a pair of receive ports to a ladspa plugin"""
  if dry_run:
    print("Connect to ladspa", receive, "to", ladspa)
    return
  jack_client.connect(receive + ':receive_1', ladspa + ':Input (Left)')
  jack_client.connect(receive + ':receive_2', ladspa + ':Input (Right)')

def connect_from_ladspa(jack_client, ladspa, send, dry_run = False):
  """connect a ladspa plugin to a pair of send ports"""
  if dry_run:
    print("Connect from ladspa", ladspa, "to", send)
    return
  jack_client.connect(ladspa + ':Output (Left)', send + ':send_1')
  jack_client.connect(ladspa + ':Output (Right)', send + ':send_2')

def connect_to_soft_left(jack_client, receive, send, dry_run = False):
  if dry_run:
    print("Connect soft left", receive, "to", send)
    return
  jack_client.connect(receive + ':receive_1', 'slight-left:Input (Left)')
  jack_client.connect('slight-left:Output (Left)', send + ':send_1')

  jack_client.connect(receive + ':receive_2', 'slight-left:Input (Right)')
  jack_client.connect('slight-left:Output (Right)', send + ':send_2')

def connect_to_soft_right(jack_client, receive, send, dry_run = False):
  if dry_run:
    print("Connect soft right", receive, "to", send)
    return
  jack_client.connect(receive + ':receive_1', 'slight-right:Input (Left)')
  jack_client.connect('slight-right:Output (Left)', send + ':send_1')

  jack_client.connect(receive + ':receive_2', 'slight-right:Input (Right)')
  jack_client.connect('slight-right:Output (Right)', send + ':send_2')
