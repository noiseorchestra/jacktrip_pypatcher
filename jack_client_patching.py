# Helper functions for autopatching JackTrip hubserver clients

import jack


class JackClientPatching:
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
            if send_port.name.startswith("jack_capture"):
                continue
            print("disconnect", my_port.name, "from", send_port.name)
            try:
                self.jackClient.disconnect(my_port, send_port)
            except Exception as e:
                print("error disconnecting, trying the other way round!", e)
                print("disconnect", send_port.name, "from", my_port.name)
                self.jackClient.disconnect(send_port, my_port)

    # Different clients have different characteristics:
    #   * jacktrip clients can have 1 or 2 channels (:receive_n, :send_n)
    #   * jacktrip receive_1 always has input
    #   * jacktrip receive_2 may or may not exist & may or may have input if it does exist
    #   * jacktrip send_1 always exist, but send_2 may not
    #   * mpg123 always sends stereo (:1, :2)
    #   * ng-jackspa always sends & receives stereo (:Input (Left), :Input (Right))

    def connect_to_centre(self, receive, send, stereo=False):
        """connect pair of receive ports to the send ports, centre panned"""
        if self.dry_run:
            print("Connect centre", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", send + ":send_1")
        if stereo:
            try:
                self.jackClient.connect(receive + ":receive_2", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect(receive + ":receive_2", send + ":send_1")
        else:
            try:
                self.jackClient.connect(receive + ":receive_1", send + ":send_2")
            except Exception as e:
                print("error making connection", e)

    def connect_mpg123_to_centre(self, mpg123, send):
        """connect an instance of mpg123-jack to a jacktrip client"""
        if self.dry_run:
            print("Connect mpg123 centre", mpg123, "to", send)
            return
        try:
            self.jackClient.connect(mpg123 + ":1", send + ":send_1")
        except jack.JackErrorCode as e:
            print("Could not find mpg123, not patching ", send)
            return
        try:
            self.jackClient.connect(mpg123 + ":2", send + ":send_2")
        except Exception as e:
            print("Patching to mono send", send)
            self.jackClient.connect(mpg123 + ":2", send + ":send_1")

    def connect_to_left(self, receive, send, stereo=False):
        """connect pair of receive ports to the send ports, left panned"""
        if self.dry_run:
            print("Connect left", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", send + ":send_1")
        if stereo:
            self.jackClient.connect(receive + ":receive_2", send + ":send_1")

    def connect_to_right(self, receive, send, stereo=False):
        """connect pair of receive ports to the send ports, right panned"""
        if self.dry_run:
            print("Connect right", receive, "to", send)
            return
        try:
            self.jackClient.connect(receive + ":receive_1", send + ":send_2")
        except Exception as e:
            print("Patching to mono send", send)
            self.jackClient.connect(receive + ":receive_1", send + ":send_1")
        if stereo:
            try:
                self.jackClient.connect(receive + ":receive_2", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect(receive + ":receive_2", send + ":send_1")

    def connect_to_ladspa(self, receive, ladspa, stereo=False):
        """connect a pair of receive ports to a ladspa plugin"""
        if self.dry_run:
            print("Connect to ladspa", receive, "to", ladspa)
            return
        self.jackClient.connect(receive + ":receive_1", ladspa + ":Input (Left)")
        if stereo:
            self.jackClient.connect(receive + ":receive_2", ladspa + ":Input (Right)")
        else:
            self.jackClient.connect(receive + ":receive_1", ladspa + ":Input (Right)")

    def connect_from_ladspa(self, ladspa, send):
        """connect a ladspa plugin to a pair of send ports"""
        if self.dry_run:
            print("Connect from ladspa", ladspa, "to", send)
            return
        self.jackClient.connect(ladspa + ":Output (Left)", send + ":send_1")
        try:
            self.jackClient.connect(ladspa + ":Output (Right)", send + ":send_2")
        except Exception as e:
            print("Patching to mono send", send)
            self.jackClient.connect(ladspa + ":Output (Right)", send + ":send_1")

    def connect_to_soft_left(self, receive, send, stereo=False):
        if self.dry_run:
            print("Connect soft left", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", "slight-left:Input (Left)")
        self.jackClient.connect("slight-left:Output (Left)", send + ":send_1")

        if stereo:
            self.jackClient.connect(receive + ":receive_2", "slight-left:Input (Right)")
            try:
                self.jackClient.connect("slight-left:Output (Right)", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect("slight-left:Output (Right)", send + ":send_1")
        else:
            self.jackClient.connect(receive + ":receive_1", "slight-left:Input (Right)")
            try:
                self.jackClient.connect("slight-left:Output (Right)", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect("slight-left:Output (Right)", send + ":send_1")

    def connect_to_soft_right(self, receive, send, stereo=False):
        if self.dry_run:
            print("Connect soft right", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", "slight-right:Input (Left)")
        self.jackClient.connect("slight-right:Output (Left)", send + ":send_1")

        if stereo:
            self.jackClient.connect(
                receive + ":receive_2", "slight-right:Input (Right)"
            )
            try:
                self.jackClient.connect("slight-right:Output (Right)", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect("slight-right:Output (Right)", send + ":send_1")
        else:
            self.jackClient.connect(
                receive + ":receive_1", "slight-right:Input (Right)"
            )
            try:
                self.jackClient.connect("slight-right:Output (Right)", send + ":send_2")
            except Exception as e:
                print("Patching to mono send", send)
                self.jackClient.connect("slight-right:Output (Right)", send + ":send_1")

    # Darkice
    def connect_darkice_to_centre(self, receive, send, stereo=False):
        """connect pair of receive ports to a jacktrip client"""
        if self.dry_run:
            print("Connect centre", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", send + ":left")
        if stereo:
            self.jackClient.connect(receive + ":receive_2", send + ":right")
        else:
            self.jackClient.connect(receive + ":receive_1", send + ":right")

    def connect_darkice_to_left(self, receive, send, stereo=False):
        """connect pair of receive ports to the send ports, left panned"""
        if self.dry_run:
            print("Connect left", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", send + ":left")
        if stereo:
            self.jackClient.connect(receive + ":receive_2", send + ":left")

    def connect_darkice_to_right(self, receive, send, stereo=False):
        """connect pair of receive ports to the send ports, right panned"""
        if self.dry_run:
            print("Connect right", receive, "to", send)
            return
        self.jackClient.connect(receive + ":receive_1", send + ":right")
        if stereo:
            self.jackClient.connect(receive + ":receive_2", send + ":right")

    def connect_darkice_from_ladspa(self, ladspa, send):
        """connect a ladspa plugin to a pair of send ports"""
        if self.dry_run:
            print("Connect from ladspa", ladspa, "to", send)
            return
        self.jackClient.connect(ladspa + ":Output (Left)", send + ":left")
        self.jackClient.connect(ladspa + ":Output (Right)", send + ":right")

    def connect_mpg123_to_darkice(self, mpg123, send):
        """connect an instance of mpg123-jack to a darkice client"""
        if self.dry_run:
            print("Connect mpg123 centre", mpg123, "to", send)
            return
        try:
            self.jackClient.connect(mpg123 + ":1", send + ":left")
            self.jackClient.connect(mpg123 + ":2", send + ":right")
        except jack.JackErrorCode as e:
            print("Could not find mpg123, not patching ", send)
            return
