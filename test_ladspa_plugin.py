import jack
import jacktrip_pypatcher
import ladspa_plugins as ladspa


def test_generate_subprocess_cmd(position=0.3):

    cmd = [
        "/home/sam/ng-jackspa/jackspa-cli",
        "-j",
        "ladspa-right-30",
        "-i",
        "0:0:0:0.3:0:0",
        "/usr/lib/ladspa/inv_input.so",
        "3301",
    ]

    assert ladspa.generate_subprocess_cmd(position) == cmd


def test_generate_port_name():

    panning_positions = [0, -0.3, 0.3, -0.6, 0.6]
    port_names = [
        "ladspa-centre",
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    assert [
        ladspa.generate_port_name(position) for position in panning_positions
    ] == port_names


# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_and_check_port():
    class LadspaClient:
        def __init__(self, name):
            self.name = name

    jackClient = None
    dry_run = True
    panning_positions = [0, -0.3, 0.3, -0.6, 0.6]
    all_existing_ladspa_ports = [LadspaClient("ladspa-centre")]

    result = [
        "ladspa-centre",
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    assert [
        ladspa.get_port(jackClient, position, all_existing_ladspa_ports, dry_run=True)
        for position in panning_positions
    ] == result


# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_ports():
    class LadspaClient:
        def __init__(self, name):
            self.name = name

    jackClient = None
    dry_run = True
    all_panning_positions = [
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
    no_of_clients = 4
    all_existing_ladspa_ports = [LadspaClient("ladspa-centre")]
    panning_positions = [
        ladspa.generate_port_name(position) for position in all_panning_positions[3:7]
    ]

    assert (
        ladspa.get_ports(
            jackClient,
            no_of_clients,
            all_panning_positions,
            all_existing_ladspa_ports,
            dry_run,
        )
        == panning_positions
    )
