# Helper functions to start/stop stereo recording of sessions

# import jack
import psutil
import subprocess

# import time


def darkice_process():
    for proc in psutil.process_iter(["pid", "name", "username", "cmdline"]):
        if proc.name() == "jack_capture":
            return proc
            if proc.cmdline()[2] == "darkice-":
                return proc


def start():
    recording_path_prefix = "/home/sam/darkice-"

    print("-- recordings --")
    if darkice_process():
        print("already started!")
    else:
        print("starting...")
        mysub = subprocess.Popen(
            [
                "jack_capture",
                "--filename-prefix",
                recording_path_prefix,
                "-S",
                "--channels",
                "2",
                "--port",
                "darkice*",
                "--daemon",
            ]
        )
        print("Recording started, process num: ", mysub.pid)


def stop():
    print("-- recordings --")
    myprocess = darkice_process()
    if not myprocess:
        print("No recording running, apparently!")
        return
    print("Stopping recording process num:", myprocess.pid)
    myprocess.kill()
