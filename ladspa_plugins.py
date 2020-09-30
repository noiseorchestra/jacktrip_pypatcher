# Helper functions plugins

import subprocess
import time

jackspa_path = "/home/sam/ng-jackspa/jackspa-cli"


def generate_port_name(panning_position):
    """Returns a ladspa port name"""
    if panning_position == 0:
        return "ladspa-centre"
    elif panning_position < 0:
        return "ladspa-left-" + str(int(abs(panning_position*100)))
    else:
        return "ladspa-right-" + str(int(panning_position*100))


def get_port(jackClient, panning_position):
    """Start a ladspa plugin if it isn't running and return port name"""
    port_name = generate_port_name(panning_position)
    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    if port_name not in [port.name for port in all_ladspa_ports]:
        start_plugin(jackClient, panning_position)
    return port_name


def generate_subprocess_cmd(panning_position):
  port_name = get_port(panning_position)
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
        print("Start ladspa plugins for 2 - 5 clients")

    cmd = generate_subprocess_cmd(panning_position)
    subprocess.Popen(cmd)
    time.sleep(0.5)

    if debug:
        all_plugins = jackClient.get_ports("ladspa.*")
        print("Running ladspa plugins:", all_plugins)
