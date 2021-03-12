import subprocess
import time
import numpy as np


class LadspaPlugins(object):
    """LadspaPlugins patching stuff"""

    def __init__(self, jackClient, jackspa_path, dry_run=False):
        super(LadspaPlugins, self).__init__()
        self.jackClient = jackClient
        self.jackspa_path = jackspa_path
        self.dry_run = dry_run

    def get_panning_positions(self, number_of_clients):
        if number_of_clients == 0:
            return []

        if number_of_clients == 1:
            return [0]

        if number_of_clients == 2:
            # Just map points between -0.5 and 0.5 for shallow 2 client panning
            return list(np.linspace(-0.5, 0.5, number_of_clients))

        if number_of_clients == 3:
            # Fixes the strange case of 3 clients
            panning_positions = list(np.linspace(-0.5, 0.5, number_of_clients))
            panning_positions + (panning_positions[0] - 0.01)
            panning_positions + (panning_positions[2] - 0.01)
            return panning_positions

        return list(np.linspace(-1, 1, number_of_clients))

    def generate_port_name(self, panning_position):
        """Returns a ladspa port name"""
        if panning_position == 0:
            return "ladspa-centre"
        elif panning_position < 0:
            return "ladspa-left-" + str(int(abs(panning_position * 100)))
        else:
            return "ladspa-right-" + str(int(panning_position * 100))

    def get_port(self, panning_position, all_ladspa_ports):
        """Start a ladspa plugin if it isn't running and return port name"""
        port_name = self.generate_port_name(panning_position)
        if port_name not in [port.name.split(":")[0] for port in all_ladspa_ports]:
            print("No ladspa port for panning position", panning_position)
            print("Starting", port_name, "now")
            self.start_plugin(panning_position)
        return port_name

    def get_ports(self, no_of_clients, all_ladspa_ports):
        panning_positions = self.get_panning_positions(no_of_clients)
        ladspa_ports = [
            self.get_port(position, all_ladspa_ports) for position in panning_positions
        ]
        return ladspa_ports

    def generate_subprocess_cmd(self, panning_position):
        port_name = self.generate_port_name(panning_position)
        return [
            self.jackspa_path,
            "-j",
            port_name,
            "-i",
            "0:0:0:" + str(panning_position) + ":0:0",
            "/usr/lib/ladspa/inv_input.so",
            "3301",
        ]

    def kill_plugins(self):
        """kill ladspa plugins"""

        if self.dry_run:
            print("Kill ladspa plugins")
            return

        subprocess.call(["killall", "jackspa-cli"])
        time.sleep(0.5)

    def start_plugin(self, panning_position):
        """start ladspa plugins for 2 and above clients of clients"""

        if self.dry_run:
            print("Start ladspa plugin for position:", panning_position)
            return

        cmd = self.generate_subprocess_cmd(panning_position)
        subprocess.Popen(cmd)
        time.sleep(0.5)
