# Helper functions plugins

import subprocess
import time

jackspa_path = "/home/sam/ng-jackspa/jackspa-cli"


def get_panning_positions(number_of_clients, all_panning_positions):
  if number_of_clients == 4:
    return all_panning_positions[3:7]
  if number_of_clients == 5:
    return [all_panning_positions[0]] + all_panning_positions[3:7]
  if number_of_clients == 6:
    return all_panning_positions[1:3] + all_panning_positions[5:9]
  if number_of_clients == 7:
    return all_panning_positions[0:3] + all_panning_positions[5:9]
  if number_of_clients == 8:
    return all_panning_positions[1:9]
  if number_of_clients == 9:
    return all_panning_positions[0:9]
  if number_of_clients == 10:
    return all_panning_positions[1:11]
  if number_of_clients == 11:
    return all_panning_positions[0:11]


def generate_port_name(panning_position):
    """Returns a ladspa port name"""
    if panning_position == 0:
        return "ladspa-centre"
    elif panning_position < 0:
        return "ladspa-left-" + str(int(abs(panning_position*100)))
    else:
        return "ladspa-right-" + str(int(panning_position*100))


def get_port(jackClient, panning_position, all_ladspa_ports, dry_run=False):
    """Start a ladspa plugin if it isn't running and return port name"""
    port_name = generate_port_name(panning_position)
    if port_name not in [port.name.split(":")[0] for port in all_ladspa_ports]:
        print("No ladspa port for panning position", panning_position)
        print("Starting", port_name, "now")
        if not dry_run:
            start_plugin(jackClient, panning_position)
    return port_name


def get_ports(jackClient, no_of_clients, all_panning_positions, all_ladspa_ports, dry_run=False):
    panning_positions = get_panning_positions(no_of_clients, all_panning_positions)
    ladspa_ports = [get_port(jackClient, position, all_ladspa_ports, dry_run) for position in panning_positions]
    return ladspa_ports


def generate_subprocess_cmd(panning_position):
  port_name = generate_port_name(panning_position)
  return [jackspa_path,
          "-j",
          port_name,
          "-i",
          "0:0:0:" + str(panning_position) + ":0:0",
          "/usr/lib/ladspa/inv_input.so",
          "3301",
          ]


def kill_plugins(jackClient, debug=True):
    """kill ladspa plugins"""

    if debug:
        print("Kill ladspa plugins")

    subprocess.call(["killall", "jackspa-cli"])
    time.sleep(0.5)

    if debug:
        all_plugins = jackClient.get_ports("ladspa.*")
        print("Running ladspa plugins:", all_plugins)


def start_plugin(jackClient, panning_position, debug=True):
    """start ladspa plugins for 2 and above clients of clients"""

    if debug:
        print("Start ladspa plugins")

    cmd = generate_subprocess_cmd(panning_position)
    subprocess.Popen(cmd)
    time.sleep(0.5)

    if debug:
        all_plugins = jackClient.get_ports("ladspa.*")
        print("Running ladspa plugins:", all_plugins)
