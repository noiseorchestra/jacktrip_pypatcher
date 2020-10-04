import ladspa_plugins as ladspa

def test_generate_subprocess_cmd(position=0.3):

    panning_positions = [
        0,
        -0.15,
        0.15,
        -0.3,
        0.3,
        -0.45,
        0.45,
        -0.6,
        0.6,
        -0.75,
        0.75,
    ]

    assert ladspa.get_panning_positions(2, panning_positions) == [-0.45, -0.46, 0.45, 0.46]
