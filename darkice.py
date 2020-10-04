class Darkice(object):
  """Darkice patching stuff"""
  def __init__(self, jackClient, port_prefix):
    super(DarkIce, self).__init__()
    self.port_prefix = port_prefix
    self.jackClient = jackClient

  def get_port(self, dry_run):
      """Get the current darkice jack port prefix"""
      darkice_ports = list(
          map(
              lambda x: x.name.split(":")[0],
              self.jackClient.get_ports(self.darkice_prefix + ".*:left"),
          )
      )

      if dry_run:
          darkice_ports = ["darkice-10545"]

      if len(darkice_ports) == 0:
          print("Start darkice first, please")
          SystemExit(1)

      return darkice_ports[0]

