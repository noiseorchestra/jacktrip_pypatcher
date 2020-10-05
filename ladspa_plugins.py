import subprocess
import time


class LadspaPlugins(object):
    """LadspaPlugins patching stuff"""

    def __init__(self, jackClient, jackspa_path, all_positions):
        super(LadspaPlugins, self).__init__()
        self.jackClient = jackClient
        self.jackspa_path = jackspa_path
        self.all_positions = all_positions

    # we could set this as an attribute and have a get_and_set() method when
    # we need to refresh the list, but this might get confusing
    def get_all_ports(self):
        return self.jackClient.get_ports("ladspa-.*")

    def get_panning_positions(self, number_of_clients):
      if number_of_clients == 2 or number_of_clients == 3:
        return [self.all_positions[5], (self.all_positions[5]-0.01),
                self.all_positions[6], (self.all_positions[6]+0.01)]
      if number_of_clients == 4:
        return self.all_positions[3:7]
      if number_of_clients == 5:
        return [self.all_positions[0]] + self.all_positions[3:7]
      if number_of_clients == 6:
        return self.all_positions[1:3] + self.all_positions[5:9]
      if number_of_clients == 7:
        return self.all_positions[0:3] + self.all_positions[5:9]
      if number_of_clients == 8:
        return self.all_positions[1:9]
      if number_of_clients == 9:
        return self.all_positions[0:9]
      if number_of_clients == 10:
        return self.all_positions[1:11]
      if number_of_clients == 11:
        return self.all_positions[0:11]

    def generate_port_name(self, panning_position):
        """Returns a ladspa port name"""
        if panning_position == 0:
            return "ladspa-centre"
        elif panning_position < 0:
            return "ladspa-left-" + str(int(abs(panning_position*100)))
        else:
            return "ladspa-right-" + str(int(panning_position*100))

    def get_port(self, panning_position, dry_run=False):
        """Start a ladspa plugin if it isn't running and return port name"""
        port_name = self.generate_port_name(panning_position)
        if port_name not in [port.name.split(":")[0] for port in self.get_all_ports()]:
            print("No ladspa port for panning position", panning_position)
            print("Starting", port_name, "now")
            if not dry_run:
                self.start_plugin(panning_position)
        return port_name

    def get_ports(self, no_of_clients, dry_run=False):
        panning_positions = self.get_panning_positions(no_of_clients)
        ladspa_ports = [self.get_port(position, dry_run) for position in panning_positions]
        return ladspa_ports

    def generate_subprocess_cmd(self, panning_position):
      port_name = self.generate_port_name(panning_position)
      return [self.jackspa_path,
              "-j",
              port_name,
              "-i",
              "0:0:0:" + str(panning_position) + ":0:0",
              "/usr/lib/ladspa/inv_input.so",
              "3301",
              ]

    def kill_plugins(self, debug=True):
        """kill ladspa plugins"""

        if debug:
            print("Kill ladspa plugins")

        subprocess.call(["killall", "jackspa-cli"])
        time.sleep(0.5)

        if debug:
            print("Running ladspa plugins:", self.get_all_ports())

    def start_plugin(self, panning_position, debug=True):
        """start ladspa plugins for 2 and above clients of clients"""

        cmd = self.generate_subprocess_cmd(panning_position)
        subprocess.Popen(cmd)
        time.sleep(0.5)

        if debug:
            print("Running ladspa plugins:", self.get_all_ports())
