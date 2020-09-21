# Helper functions plugins

import subprocess
import time

jackspa_path = '/home/sam/ng-jackspa/jackspa-cli'

def kill_plugins(jackClient, debug = True):
  """kill ladspa plugins"""

  if debug:
    print("Kill ladspa plugins")

  subprocess.call(['killall', 'jackspa-cli'])
  time.sleep(0.5)

  if debug:
    all_plugins = jackClient.get_ports('ladspa.*')
    print('Running ladspa plugins:', all_plugins)

def start_plugins_2(jackClient, debug = True):
  """start ladspa plugins for 2 and above clients of clients"""

  if debug:
    print("Start ladspa plugins for 2 - 5 clients")

  subprocess.Popen([jackspa_path, '-j', 'ladspa-left-30', '-i', '0:0:0:-0.30:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-right-30', '-i', '0:0:0:0.30:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-left-60', '-i', '0:0:0:-0.60:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-right-60', '-i', '0:0:0:0.60:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-left-45', '-i', '0:0:0:-0.45:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-right-45', '-i', '0:0:0:0.45:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  time.sleep(0.5)

  if debug:
    all_plugins = jackClient.get_ports('ladspa.*')
    print('Running ladspa plugins:', all_plugins)



def start_plugins_5(jackClient, debug = True):
  """start ladspa plugins for 5 and above clients"""

  if debug:
    print("Start ladspa plugins for 5 - 9 clients")

  subprocess.Popen([jackspa_path, '-j', 'ladspa-centre', '-i', '0:0:0:0:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-left-15', '-i', '0:0:0:-0.15:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-right-15', '-i', '0:0:0:0.15:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  time.sleep(0.5)

  if debug:
    all_plugins = jackClient.get_ports('ladspa.*')
    print('Running ladspa plugins:', all_plugins)

def start_plugins_10(jackClient, debug = True):
  """start ladspa plugins for 10 and above clients"""

  if debug:
    print("Start ladspa plugins for 10 - 11 clients")

  subprocess.Popen([jackspa_path, '-j', 'ladspa-left-75', '-i', '0:0:0:-0.75:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  subprocess.Popen([jackspa_path, '-j', 'ladspa-right-75', '-i', '0:0:0:0.75:0:0', '/usr/lib/ladspa/inv_input.so', '3301'])
  time.sleep(0.5)

  if debug:
    all_plugins = jackClient.get_ports('ladspa.*')
    print('Running ladspa plugins:', all_plugins)
