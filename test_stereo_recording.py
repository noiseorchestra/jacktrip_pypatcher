from unittest.mock import Mock
from stereo_recording import StereoRecording
import pytest


def test_get_filename_prefix(freezer):
    stereo_recording = StereoRecording("/home/sam/recordings/audio/", dry_run=True)
    freezer.move_to("2020-10-15 12:54")

    filename_prefix = "/home/sam/recordings/audio/2020_10_15_1254-"
    assert stereo_recording.get_filename_prefix() == filename_prefix


def test_generate_subprocess_cmd(freezer):

    stereo_recording = StereoRecording("/home/sam/recordings/audio/", dry_run=True)
    freezer.move_to("2020-10-15 12:54")

    cmd = [
        "jack_capture",
        "--filename-prefix",
        "/home/sam/recordings/audio/2020_10_15_1254-",
        "-S",
        "--channels",
        "2",
        "--port",
        "darkice*",
        "--daemon",
    ]

    assert stereo_recording.generate_subprocess_cmd() == cmd
