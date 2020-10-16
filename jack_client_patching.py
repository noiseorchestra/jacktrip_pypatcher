# Helper functions for autopatching JackTrip hubserver clients

import jack


class JackClientPatching:
    """Helper object to do all the jack client patching"""

    def __init__(self, jackClient, dry_run):
        super(JackClientPatching, self).__init__()
        self.jackClient = jackClient
        self.connections = []
        self.dry_run = dry_run

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

    def connect_ports(self, receive, send):

        receive_ports = self.jackClient.get_ports(receive)
        send_ports = self.jackClient.get_ports(send)

        print("Connecting", receive_ports, "to", send_ports)

        if (len(receive_ports) == 0) or (len(send_ports) == 0):
            print("Not connecting, both clients must have valid ports")
            return

        receive_stereo = len(receive_ports) == 2
        send_stereo = len(send_ports) == 2

        try:
            # we always connect receive_port[0] to send_port[0]
            self.jackClient.connect(receive_ports[0], send_ports[0])
            if receive_stereo and send_stereo:
                print("Connecting Stereo receive to Stereo send")
                self.jackClient.connect(receive_ports[1], send_ports[1])
            elif receive_stereo and not send_stereo:
                print("Connecting Stereo receive to Mono send")
                self.jackClient.connect(receive_ports[1], send_ports[0])
            elif not receive_stereo and send_stereo:
                print("Connecting Mono receive to Stereo send")
                self.jackClient.connect(receive_ports[0], send_ports[1])
            else:
                print("Connecting Mono receive to Mono send")
        except Exception as e:
            print("Error connecting ports:", e)

    def jacktrip_receive(self, port):
        return port + ":receive_.*"

    def jacktrip_send(self, port):
        return port + ":send_.*"

    def ladspa_receive(self, port):
        return port + ":Output.*"

    def ladspa_send(self, port):
        return port + ":Input.*"

    def darkice_send(self, port):
        return port + ".*"

    def set_darkice_connections(self, ladspa_ports, darkice):
        """append darkice connections to connections list"""
        for ladspa in ladspa_ports:
            self.connections.append(
                (self.ladspa_receive(ladspa), self.darkice_send(darkice))
            )

    def set_connections_2_clients(self, jacktrip_ports, ladspa_ports):

        jacktrip_receive_1 = self.jacktrip_receive(jacktrip_ports[0])
        jacktrip_receive_2 = self.jacktrip_receive(jacktrip_ports[1])
        jacktrip_send_1 = self.jacktrip_send(jacktrip_ports[0])
        jacktrip_send_2 = self.jacktrip_send(jacktrip_ports[1])

        self.connections.append((jacktrip_receive_1, jacktrip_send_2))
        self.connections.append((jacktrip_receive_2, jacktrip_send_1))
        self.connections.append((jacktrip_receive_1, self.ladspa_send(ladspa_ports[0])))
        self.connections.append((jacktrip_receive_2, self.ladspa_send(ladspa_ports[1])))

    def set_connections_3_clients(self, jacktrip_ports, ladspa_ports):

        jacktrip_receive_1 = self.jacktrip_receive(jacktrip_ports[0])
        jacktrip_receive_2 = self.jacktrip_receive(jacktrip_ports[1])
        jacktrip_receive_3 = self.jacktrip_receive(jacktrip_ports[2])
        jacktrip_send_1 = self.jacktrip_send(jacktrip_ports[0])
        jacktrip_send_2 = self.jacktrip_send(jacktrip_ports[1])
        jacktrip_send_3 = self.jacktrip_send(jacktrip_ports[2])

        for ladspa_port in ladspa_ports[0:3]:
            self.connections.append((jacktrip_receive_1, self.ladspa_send(ladspa_port)))

        self.connections.append((jacktrip_receive_2, self.ladspa_send(ladspa_ports[3])))
        self.connections.append((jacktrip_receive_3, self.ladspa_send(ladspa_ports[4])))

        self.connections.append((self.ladspa_receive(ladspa_ports[3]), jacktrip_send_1))
        self.connections.append((self.ladspa_receive(ladspa_ports[4]), jacktrip_send_1))

        self.connections.append((self.ladspa_receive(ladspa_ports[1]), jacktrip_send_2))
        self.connections.append((self.ladspa_receive(ladspa_ports[4]), jacktrip_send_2))

        self.connections.append((self.ladspa_receive(ladspa_ports[3]), jacktrip_send_3))
        self.connections.append((self.ladspa_receive(ladspa_ports[2]), jacktrip_send_3))

    def set_all_connections(self, jacktrip_ports, ladspa_ports):
        """append all connections between JackTrip clients & ladspa ports"""

        if len(jacktrip_ports) == 2:
            self.set_connections_2_clients(jacktrip_ports, ladspa_ports)

        if len(jacktrip_ports) == 3:
            self.set_connections_3_clients(jacktrip_ports, ladspa_ports)

        if len(jacktrip_ports) > 3:
            for i, ladspa in enumerate(ladspa_ports):
                jacktrip_receive = self.jacktrip_receive(jacktrip_ports[i])
                ladspa_send = self.ladspa_send(ladspa)
                self.connections.append((jacktrip_receive, ladspa_send))
                for jacktrip_port in jacktrip_ports:
                    if jacktrip_port == jacktrip_ports[i]:
                        continue
                    ladspa_receive = self.ladspa_receive(ladspa)
                    jacktrip_send = self.jacktrip_send(jacktrip_port)
                    self.connections.append((ladspa_receive, jacktrip_send))

    def make_all_connections(self):
        if self.dry_run:
            print("Make all connections")
            print(self.connections)
            return

        [self.connect_ports(c[0], c[1]) for c in self.connections]

    def connect_to_centre(self, receive, send):
        """connect receive port/s to centre send"""
        if self.dry_run:
            print("Connect centre", receive, "to", send)
            return

        self.connect_ports(receive + ":receive_.*", send + ":send_.*")

    def connect_mpg123_to_centre(self, mpg123, send):
        """connect an instance of mpg123-jack to a jacktrip client"""
        if self.dry_run:
            print("Connect mpg123 centre", mpg123, "to", send)
            return

        self.connect_ports(mpg123 + ":.*", send + ":send_.*")

    def connect_darkice_to_centre(self, receive, send):
        if self.dry_run:
            print("Connect centre", receive, "to", send)
            return

        self.connect_ports(receive + ":receive_.*", send + ".*")

    def connect_mpg123_to_darkice(self, mpg123, send):
        """connect an instance of mpg123-jack to a darkice client"""
        if self.dry_run:
            print("Connect mpg123 centre", mpg123, "to", send)
            return
        try:
            self.connect_ports(mpg123 + ".*", send + ".*")
        except jack.JackErrorCode as e:
            print("Could not find mpg123, not patching ", send)
            return
