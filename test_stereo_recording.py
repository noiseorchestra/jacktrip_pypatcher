from unittest.mock import Mock
from stereo_recording import StereoRecording


def test_get_filename_prefix():
    stereo_recording = StereoRecording("/home/sam/recordings/audio/", dry_run=True)
    mock = Mock()
    mock.return_value = "2020_10_15_1254"
    stereo_recording.get_time_string = mock
    filename_prefix = "/home/sam/recordings/audio/2020_10_15_1254-"
    assert stereo_recording.get_filename_prefix() == filename_prefix


def test_generate_subprocess_cmd():

    stereo_recording = StereoRecording("/home/sam/recordings/audio/", dry_run=True)
    mock = Mock()
    mock.return_value = "2020_10_15_1254"
    stereo_recording.get_time_string = mock

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
