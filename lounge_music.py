import psutil
import subprocess
import time


class LoungeMusic(object):
    """Lounge music patching stuff"""

    def __init__(self, jackClient, port, file_path):
        super(LoungeMusic, self).__init__()
        self.jackClient = jackClient
        self.port = port
        self.file_path = file_path
        self.debug = False

    def get_command(self):
        """Get the command to start mpg123"""
        return [
            "mpg123-jack",
            "--name",
            self.port,
            "--no-control",
            "-q",
            "--loop",
            "-1",
            self.file_path,
        ]

    def get_all_ports(self):
        """Return all lounge_music ports"""
        return self.jackClient.get_ports(self.port + ".*")

    def check_the_music(self):
        """Check if lounge_music is playing"""
        if len(self.get_all_ports()) == 0:
            count = 0
            while count < 3:
                subprocess.Popen(self.get_command())
                count += 1
                time.sleep(0.5)

    def start_the_music_with_retries(self, debug=True):
        """start looping the hold music, if it isn't already playing"""

        if len(self.get_all_ports()) > 0:
            if debug:
                print("Lounge music already playing!")
            return

        if debug:
            print("Start the lounge music please!")

        subprocess.Popen(self.get_command())
        time.sleep(0.5)

        self.check_the_music()

        if debug:
            print(len(self.get_all_ports()))

    def kill_the_music(self, debug=True):
        """kill the hold music, if it's playing"""

        if len(self.get_all_ports()) == 0:
            if debug:
                print("Lounge music is not playing!")
            return

        if debug:
            print("Kill the lounge music please!")

        for proc in psutil.process_iter():
            if "mpg123.bin" in proc.name():
                if self.port in proc.cmdline():
                    print("Killing lounge music process id: ", proc.pid)
                    proc.terminate()

        time.sleep(0.1)

        if debug:
            print(len(self.get_all_ports()))
