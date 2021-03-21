# Helper functions for autopatching JackTrip hubserver clients

import jack


class JackClientPatching:
    """Helper object to do all the jack client patching"""

    def __init__(self, jackClient, dry_run):
        super(JackClientPatching, self).__init__()
        self.jackClient = jackClient
        self.connections = []
        self.dry_run = dry_run

    def _jacktrip_receive(self, port):
        return port + ":receive_.*"

    def _jacktrip_send(self, port):
        return port + ":send_.*"

    def _ladspa_receive(self, port):
        return port + ":Output.*"

    def _ladspa_send(self, port):
        return port + ":Input.*"

    def _darkice_send(self, port):
        return port + ".*"

    def _mpg123_send(self, port):
        return port + ".*"

    def _connect_ports(self, receive, send):
        """connect the jack ports of stereo or mono clients"""

        receive_ports = self.jackClient.get_ports(receive)
        send_ports = self.jackClient.get_ports(send)

        if (len(receive_ports) == 0) or (len(send_ports) == 0):
            print("Not connecting, both clients must have valid ports")
            return

        receive_stereo = len(receive_ports) == 2
        send_stereo = len(send_ports) == 2

        try:
            # we always connect receive_port[0] to send_port[0]
            print("Connecting", receive_ports[0].name, "to", send_ports[0].name)
            self.jackClient.connect(receive_ports[0], send_ports[0])
            if receive_stereo and send_stereo:
                print("Connecting", receive_ports[1].name, "to", send_ports[1].name)
                self.jackClient.connect(receive_ports[1], send_ports[1])
            elif receive_stereo and not send_stereo:
                print("Connecting", receive_ports[1].name, "to", send_ports[0].name)
                self.jackClient.connect(receive_ports[1], send_ports[0])
            elif not receive_stereo and send_stereo:
                print("Connecting", receive_ports[0].name, "to", send_ports[1].name)
                self.jackClient.connect(receive_ports[0], send_ports[1])

        except Exception as e:
            print("Error connecting ports:", e)

    def _set_darkice_connections_one_client(
        self, jacktrip_ports, lounge_music, darkice
    ):

        jacktrip_receive = self._jacktrip_receive(jacktrip_ports[0])
        darkice_send = self._darkice_send(darkice)
        lounge_music_receive = self._mpg123_send(lounge_music)

        self.connections.append((jacktrip_receive, darkice_send))
        self.connections.append((lounge_music_receive, darkice_send))

    def _set_connections_one_client(self, jacktrip_ports, lounge_music):

        jacktrip_receive = self._jacktrip_receive(jacktrip_ports[0])
        jacktrip_send = self._jacktrip_send(jacktrip_ports[0])
        lounge_music_receive = self._mpg123_send(lounge_music)

        self.connections.append((lounge_music_receive, jacktrip_send))
        self.connections.append((jacktrip_receive, jacktrip_send))

    def _set_connections_two_clients(self, jacktrip_ports, ladspa_ports):

        jacktrip_receive_1 = self._jacktrip_receive(jacktrip_ports[0])
        jacktrip_receive_2 = self._jacktrip_receive(jacktrip_ports[1])
        jacktrip_send_1 = self._jacktrip_send(jacktrip_ports[0])
        jacktrip_send_2 = self._jacktrip_send(jacktrip_ports[1])

        self.connections.append((jacktrip_receive_1, jacktrip_send_2))
        self.connections.append((jacktrip_receive_2, jacktrip_send_1))
        self.connections.append(
            (jacktrip_receive_1, self._ladspa_send(ladspa_ports[0]))
        )
        self.connections.append(
            (jacktrip_receive_2, self._ladspa_send(ladspa_ports[1]))
        )

    def _set_connections_three_clients(self, jacktrip_ports, ladspa_ports):

        jacktrip_receive_1 = self._jacktrip_receive(jacktrip_ports[0])
        jacktrip_receive_2 = self._jacktrip_receive(jacktrip_ports[1])
        jacktrip_receive_3 = self._jacktrip_receive(jacktrip_ports[2])
        jacktrip_send_1 = self._jacktrip_send(jacktrip_ports[0])
        jacktrip_send_2 = self._jacktrip_send(jacktrip_ports[1])
        jacktrip_send_3 = self._jacktrip_send(jacktrip_ports[2])

        for ladspa_port in ladspa_ports[0:3]:
            self.connections.append(
                (jacktrip_receive_1, self._ladspa_send(ladspa_port))
            )

        self.connections.append(
            (jacktrip_receive_2, self._ladspa_send(ladspa_ports[3]))
        )
        self.connections.append(
            (jacktrip_receive_3, self._ladspa_send(ladspa_ports[4]))
        )

        self.connections.append(
            (self._ladspa_receive(ladspa_ports[3]), jacktrip_send_1)
        )
        self.connections.append(
            (self._ladspa_receive(ladspa_ports[4]), jacktrip_send_1)
        )

        self.connections.append(
            (self._ladspa_receive(ladspa_ports[1]), jacktrip_send_2)
        )
        self.connections.append(
            (self._ladspa_receive(ladspa_ports[4]), jacktrip_send_2)
        )

        self.connections.append(
            (self._ladspa_receive(ladspa_ports[3]), jacktrip_send_3)
        )
        self.connections.append(
            (self._ladspa_receive(ladspa_ports[2]), jacktrip_send_3)
        )

    def disconnect_all(self, my_port):
        """disconnect everything from a port"""
        if self.dry_run:
            print("Disconnect all ports (except jack_capture) from", my_port)
            return
        send_ports = self.jackClient.get_all_connections(my_port)
        for send_port in send_ports:
            # do not disconnect from jack_capture ports
            # they do auto-reconnect, but the disconnection is not reliable
            if send_port.name.startswith("jack_capture"):
                continue
            print("disconnect", my_port.name, "from", send_port.name)
            try:
                self.jackClient.disconnect(my_port, send_port)
            except Exception as e:
                print("error disconnecting, trying the other way round!", e)
                print("disconnect", send_port.name, "from", my_port.name)
                self.jackClient.disconnect(send_port, my_port)

    def set_darkice_connections(
        self, ladspa_ports, darkice, jacktrip_ports=[], lounge_music=None
    ):

        if len(jacktrip_ports) == 1:
            self._set_darkice_connections_one_client(
                jacktrip_ports, lounge_music, darkice
            )
            return

        for ladspa in ladspa_ports:
            self.connections.append(
                (self._ladspa_receive(ladspa), self._darkice_send(darkice))
            )

    def set_client_connections(self, jacktrip_ports, ladspa_ports, lounge_music=None):
        """set all connections between JackTrip clients & ladspa ports"""

        if len(jacktrip_ports) == 1:
            self._set_connections_one_client(jacktrip_ports, lounge_music)

        if len(jacktrip_ports) == 2:
            self._set_connections_two_clients(jacktrip_ports, ladspa_ports)

        if len(jacktrip_ports) == 3:
            self._set_connections_three_clients(jacktrip_ports, ladspa_ports)

        if len(jacktrip_ports) > 3:
            for i, ladspa in enumerate(ladspa_ports):
                jacktrip_receive = self._jacktrip_receive(jacktrip_ports[i])
                ladspa_send = self._ladspa_send(ladspa)
                self.connections.append((jacktrip_receive, ladspa_send))
                for jacktrip_port in jacktrip_ports:
                    if jacktrip_port == jacktrip_ports[i]:
                        continue
                    ladspa_receive = self._ladspa_receive(ladspa)
                    jacktrip_send = self._jacktrip_send(jacktrip_port)
                    self.connections.append((ladspa_receive, jacktrip_send))

    def make_connections(self):
        """make all connections"""

        if self.dry_run:
            print("Make all connections")
            print(self.connections)
            return

        [self._connect_ports(c[0], c[1]) for c in self.connections]
