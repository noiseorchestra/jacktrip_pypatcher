from ladspa_plugins import LadspaPlugins
from unittest.mock import Mock


def test_generate_subprocess_cmd(position=0.3):

    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [], dry_run=True)

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

    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [], dry_run=True)
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
    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [], dry_run=True)
    panning_positions = [0, -0.3, 0.3, -0.6, 0.6]
    ladspa_client = Mock()
    ladspa_client.name = "ladspa-centre"
    all_existing_ladspa_ports = [ladspa_client]

    result = [
        "ladspa-centre",
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    assert [
        ladspa.get_port(position, all_existing_ladspa_ports)
        for position in panning_positions
    ] == result


# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_ports():
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
    ladspa = LadspaPlugins(
        None, "/home/sam/ng-jackspa/jackspa-cli", all_panning_positions, dry_run=True
    )
    no_of_clients = 4

    all_existing_ladspa_ports = [
        Mock(),
        Mock(),
    ]
    all_existing_ladspa_ports[0].name = "ladspa-centre"
    all_existing_ladspa_ports[1].name = "ladspa-left-30"

    panning_positions = [
        ladspa.generate_port_name(position) for position in all_panning_positions[3:7]
    ]

    assert (
        ladspa.get_ports(no_of_clients, all_existing_ladspa_ports,) == panning_positions
    )
