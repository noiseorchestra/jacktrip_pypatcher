# Helper functions for autopatching JackTrip hubserver clients

import jack

class JackClientPatching():
  """Helper object to do all the jack client patching"""
  def __init__(self, jackClient, dry_run):
    super(JackClientPatching, self).__init__()
    self.jackClient = jackClient
    self.dry_run = dry_run

  def disconnect_all(self, my_port):
    """disconnect everything from a port"""
    send_ports = self.jackClient.get_all_connections(my_port)
    for send_port in send_ports:
      # do not disconnect from jack_capture ports
      # they do auto-reconnect, but the disconnection is not reliable
      if send_port.name.startswith('jack_capture'):
        continue
      print('disconnect', my_port.name, 'from', send_port.name)
      try:
        self.jackClient.disconnect(my_port, send_port)
      except Exception as e:
        print('error disconnecting, trying the other way round!', e)
        print('disconnect', send_port.name, 'from', my_port.name)
        self.jackClient.disconnect(send_port, my_port)

  # TODO:
  #   * Probably better to just pass the jack clients directly into these methods
  #   * Check naming makes sense
  #   * I think some of these could be removed if we have some more generic and reusable methods

  def connect_ports(self, receive_ports, send_ports):
    print('Connecting', receive_ports, 'to', send_ports)

    receive_stereo = True if len(receive_ports) == 2 else False
    send_stereo = True if len(send_ports) == 2 else False

    if receive_stereo and send_stereo:
      print('Connecting Stereo receive to Stereo send')
      self.jackClient.connect(receive_ports[0], send_ports[0])
      self.jackClient.connect(receive_ports[1], send_ports[1])
    if receive_stereo and not send_stereo:
      print('Connecting Stereo receive to Mono send')
      self.jackClient.connect(receive_ports[0], send_ports[0])
      self.jackClient.connect(receive_ports[1], send_ports[0])
    if not receive_stereo and send_stereo:
      print('Connecting Mono receive to Stereo send')
      self.jackClient.connect(receive_ports[0], send_ports[0])
      self.jackClient.connect(receive_ports[0], send_ports[1])
    if not receive_stereo and not send_stereo:
      print('Connecting Mono receive to Mono send')
      self.jackClient.connect(receive_ports[0], send_ports[0])
    else:
      print("Could not connect ports")

  def connect_to_centre(self, receive, send):
    """connect receive port/s to centre send"""
    if self.dry_run:
      print("Connect centre", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + ':send_.*')

    self.connect_ports(receive_ports, send_ports)

  def connect_mpg123_to_centre(self, mpg123, send):
    """connect an instance of mpg123-jack to a jacktrip client"""
    if self.dry_run:
      print("Connect mpg123 centre", mpg123, "to", send)
      return

    receive_ports = self.jackClient.get_ports(mpg123 + ':.*')
    send_ports = self.jackClient.get_ports(send + ':send_.*')

    self.connect_ports(receive_ports, send_ports)

  def connect_to_left(self, receive, send):
    """connect receive port/s to left send"""
    if self.dry_run:
      print("Connect left", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + ':send_1')

    self.connect_ports(receive_ports, send_ports)

  def connect_to_right(self, receive, send):
    """connect receive port/s to right send"""
    if self.dry_run:
      print("Connect right", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + ':send_.*')

    if len(send_ports) == 2:
      send_ports = [send_ports[1]]

    self.connect_ports(receive_ports, send_ports)

  def connect_to_ladspa(self, receive, ladspa):
    """connect receive port/s to a ladspa plugin"""
    if self.dry_run:
      print("Connect to ladspa", receive, "to", ladspa)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(ladspa + ':Input.*')

    self.connect_ports(receive_ports, send_ports)

  def connect_from_ladspa(self, ladspa, send):
    """connect a ladspa plugin to send port/s"""
    if self.dry_run:
      print("Connect from ladspa", ladspa, "to", send)
      return

    receive_ports = self.jackClient.get_ports(ladspa + ':Output.*')
    send_ports = self.jackClient.get_ports(send + ':send_.*')

    self.connect_ports(receive_ports, send_ports)

  def connect_darkice_to_centre(self, receive, send):
    if self.dry_run:
      print("Connect centre", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + '.*')

    self.connect_ports(receive_ports, send_ports)

  def connect_darkice_to_left(self, receive, send):
    """connect pair of receive ports to the send ports, left panned"""
    if self.dry_run:
      print("Connect left", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + ':left')

    self.connect_ports(receive_ports, send_ports)

  def connect_darkice_to_right(self, receive, send):
    """connect pair of receive ports to the send ports, right panned"""
    if self.dry_run:
      print("Connect right", receive, "to", send)
      return

    receive_ports = self.jackClient.get_ports(receive + ':receive_.*')
    send_ports = self.jackClient.get_ports(send + ':right')

    self.connect_ports(receive_ports, send_ports)

  def connect_darkice_from_ladspa(self, ladspa, send):
    """connect a ladspa plugin to a pair of send ports"""
    if self.dry_run:
      print("Connect from ladspa", ladspa, "to", send)
      return

    self.jackClient.connect(ladspa + ':Output (Left)', send + ':left')
    self.jackClient.connect(ladspa + ':Output (Right)', send + ':right')

  def connect_mpg123_to_darkice(self, mpg123, send):
    """connect an instance of mpg123-jack to a darkice client"""
    if self.dry_run:
      print("Connect mpg123 centre", mpg123, "to", send)
      return
    try:
      self.jackClient.connect(mpg123 + ':1', send + ':left')
      self.jackClient.connect(mpg123 + ':2', send + ':right')
    except jack.JackErrorCode as e:
      print('Could not find mpg123, not patching ', send)
      return
