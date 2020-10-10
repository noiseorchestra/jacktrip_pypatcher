import psutil
import subprocess
import time


class LoungeMusic(object):
    """Lounge music patching stuff"""

    def __init__(self, jackClient, port, file_path, dry_run):
        super(LoungeMusic, self).__init__()
        self.jackClient = jackClient
        self.port = port
        self.file_path = file_path
        self.dry_run = dry_run

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

        ports = self.jackClient.get_ports(self.port + ".*")

        if self.dry_run:
            print("Called lounge_music.get_all_ports()")
            print("Response:", ports)

        return ports

    def start_the_music(self):
        if self.dry_run:
            print("Start lounge music!")
            return
        subprocess.Popen(self.get_command())
        time.sleep(0.5)

    def start_the_music_with_retries(self, retries=3):
        """start looping the hold music, if it isn't already playing"""

        print("Start lounge music with", retries, "retries")
        port_count = len(self.get_all_ports())

        if port_count > 0:
            print("Lounge music already playing!")
            return

        retry_count = 0

        while port_count == 0 and retry_count < retries:
            retry_count += 1
            self.start_the_music()
            port_count = len(self.get_all_ports())

        if port_count == 0:
            print("WARNING: Could not start lounge music")
        else:
            print("Lounge music started")

    def kill_the_music(self):
        """kill the hold music, if it's playing"""

        if self.dry_run:
            print("Kill the music")
            return

        no_of_ports = len(self.get_all_ports())

        if no_of_ports == 0:
            print("Lounge music is not playing!")
            return
        else:
            print("Kill the lounge music please!")

        for proc in psutil.process_iter():
            if "mpg123.bin" in proc.name():
                if self.port in proc.cmdline():
                    print("Killing lounge music process id: ", proc.pid)
                    proc.terminate()

        time.sleep(0.1)
