from stereo_recording import StereoRecording


def test_generate_subprocess_cmd():

    stereo_recording = StereoRecording("/home/sam/darkice-", dry_run=True)
    cmd = [
        "jack_capture",
        "--filename-prefix",
        "/home/sam/darkice-",
        "-S",
        "--channels",
        "2",
        "--port",
        "darkice*",
        "--daemon",
    ]

    assert stereo_recording.generate_subprocess_cmd() == cmd
