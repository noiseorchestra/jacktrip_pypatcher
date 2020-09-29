# Helper functions plugins

import subprocess
import time
import jacktrip_pypatcher as jp

jackspa_path = "/home/sam/ng-jackspa/jackspa-cli"


def generate_subprocess_cmd(position):
  port_name = jp.get_ladspa_port_name(position)
  return [jackspa_path,
          "-j",
          port_name,
          "-i",
          "0:0:0:" + str(position) + ":0:0",
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


def start_plugins(jackClient, panning_positions, debug=True):
    """start ladspa plugins for 2 and above clients of clients"""

    if debug:
        print("Start ladspa plugins for 2 - 5 clients")

    for position in panning_positions:
        cmd = generate_subprocess_cmd(position)
        subprocess.Popen(cmd)
    time.sleep(0.5)

    if debug:
        all_plugins = jackClient.get_ports("ladspa.*")
        print("Running ladspa plugins:", all_plugins)
