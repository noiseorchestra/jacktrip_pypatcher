import stereo_recording

def test_get_command():

    recording_path_prefix = "/home/sam/darkice-"
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

    assert stereo_recording.get_command(recording_path_prefix) == cmd
