# Helper functions to start/stop stereo recording of sessions

# import jack
import psutil
import subprocess


class StereoRecording(object):
    """Record stereo mix"""

    def __init__(self, recording_path_prefix, dry_run):
        super(StereoRecording, self).__init__()
        self.recording_path_prefix = recording_path_prefix
        self.dry_run = dry_run

    def generate_subprocess_cmd(self):
        return [
            "jack_capture",
            "--filename-prefix",
            self.recording_path_prefix,
            "-S",
            "--channels",
            "2",
            "--port",
            "darkice*",
            "--daemon",
        ]

    def darkice_process(self):
        for proc in psutil.process_iter(["pid", "name", "username", "cmdline"]):
            if proc.name() == "jack_capture":
                return proc
                if proc.cmdline()[2] == "darkice-":
                    return proc

    def start(self):
        if self.dry_run:
            print("Start recording if not running already")
            return
        print("-- recordings --")
        if self.darkice_process():
            print("already started!")
        else:
            print("starting...")
            mysub = subprocess.Popen(self.generate_subprocess_cmd())
            print("Recording started, process num: ", mysub.pid)

    def stop(self):
        if self.dry_run:
            print("Stop recording if not stopped already")
            return
        print("-- recordings --")
        myprocess = self.darkice_process()
        if not myprocess:
            print("No recording running, apparently!")
            return
        print("Stopping recording process num:", myprocess.pid)
        myprocess.kill()
