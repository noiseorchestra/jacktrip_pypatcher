# Helper functions for the lounge music

import jack
import psutil
import subprocess
import time


def get_command(hold_music, hold_music_file_path):
    return [
        "mpg123-jack",
        "--name",
        hold_music,
        "--no-control",
        "-q",
        "--loop",
        "-1",
        hold_music_file_path,
    ]


def check_the_music(jackClient, hold_music, hold_music_file_path):
    all_hold_music_ports = jackClient.get_ports(hold_music + ".*")
    cmd = get_command(hold_music, hold_music_file_path)
    if len(all_hold_music_ports) == 0:
        count = 0
        while count < 3:
            subprocess.Popen(cmd)
            count += 1
            time.sleep(0.5)


def start_the_music_with_retries(jackClient, hold_music, debug=True):
    """start looping the hold music, if it isn't already playing"""
    hold_music_file_path = "/home/sam/lounge-music.mp3"

    all_hold_music_ports = jackClient.get_ports(hold_music + ".*")

    if len(all_hold_music_ports) > 0:
        if debug:
            print("Lounge music already playing!")
        return

    if debug:
        print("Start the lounge music please!")

    cmd = get_command(hold_music, hold_music_file_path)
    # TODO: change to `mpg123.bin -o jack`
    subprocess.Popen(cmd)
    # wait for the jack client to register
    time.sleep(2)

    check_the_music(jackClient, hold_music, hold_music_file_path)

    if debug:
        all_hold_music_ports = jackClient.get_ports(hold_music + ".*")
        print(len(all_hold_music_ports))


def kill_the_music(jackClient, port, debug=True):
    """kill the hold music, if it's playing"""
    all_hold_music_ports = jackClient.get_ports(port + ".*")

    if len(all_hold_music_ports) == 0:
        if debug:
            print("Lounge music is not playing!")
        return

    if debug:
        print("Kill the lounge music please!")

    for proc in psutil.process_iter():
        if "mpg123.bin" in proc.name():
            if port in proc.cmdline():
                print("Killing lounge music process id: ", proc.pid)
                proc.terminate()
                # proc.wait()
    time.sleep(0.1)

    if debug:
        all_hold_music_ports = jackClient.get_ports(port + ".*")
        print(len(all_hold_music_ports))
