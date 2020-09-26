#!/usr/bin/env python3

"""Create a JACK client that prints a lot of information.

This client registers all possible callbacks (except the process
callback and the timebase callback, which would be just too much noise)
and prints some information whenever they are called.

NICKED FROM chatty_client.py

"""
from __future__ import print_function  # only needed for Python 2.x
import jack
from time import sleep
import jacktrip_pypatcher as jtp
from pathlib import Path

print("setting error/info functions")


@jack.set_error_function
def error(msg):
    print("Error:", msg)


@jack.set_info_function
def info(msg):
    print("Info:", msg)


print("starting chatty client")

client = jack.Client("Chatty-Client")

if client.status.server_started:
    print("JACK server was started")
else:
    print("JACK server was already running")
if client.status.name_not_unique:
    print("unique client name generated:", client.name)


print("registering callbacks")


@client.set_client_registration_callback
def client_registration(name, register):
    print("client", repr(name), ["unregistered", "registered"][register])
    print(name, " starts with '..'? (therefore JT client?)", name.startswith(".."))
    if name.startswith(".."):
        print("touching")
        touch_path = Path("/var/tmp/jacktrip_pypatcher")
        touch_path.touch()


@client.set_port_connect_callback
def port_connect(a, b, connect):
    print(["disconnected", "connected"][connect], a, "and", b)


print("activating JACK")
with client:
    while True:
        sleep(0.1)
