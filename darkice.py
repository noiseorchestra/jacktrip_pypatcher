class Darkice(object):
    """Darkice patching stuff"""

    def __init__(self, jackClient, port_prefix, dry_run=False):
        super(Darkice, self).__init__()
        self.port_prefix = port_prefix
        self.jackClient = jackClient
        self.dry_run = dry_run

    def get_port(self):
        """Get the current darkice jack port prefix"""

        if self.dry_run:
            darkice_ports = ["darkice-10545"]
            return darkice_ports[0]

        darkice_ports = list(
            map(
                lambda x: x.name.split(":")[0],
                self.jackClient.get_ports(self.port_prefix + ".*:left"),
            )
        )

        if len(darkice_ports) == 0:
            print("Start darkice first, please")
            SystemExit(1)

        return darkice_ports[0]
