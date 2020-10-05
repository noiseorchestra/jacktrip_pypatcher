from ladspa_plugins import LadspaPlugins

def test_generate_subprocess_cmd(position=0.3):

    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [])

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

    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [])
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

    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", [])
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
        ladspa.get_port(position, all_existing_ladspa_ports, dry_run=True)
        for position in panning_positions
    ] == result


# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_ports():
    class LadspaClient:
        def __init__(self, name):
            self.name = name

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
    ladspa = LadspaPlugins(None, "/home/sam/ng-jackspa/jackspa-cli", all_panning_positions)
    no_of_clients = 4
    all_existing_ladspa_ports = [LadspaClient("ladspa-centre"), LadspaClient("ladspa-left-30")]
    panning_positions = [
        ladspa.generate_port_name(position) for position in all_panning_positions[3:7]
    ]

    assert (
        ladspa.get_ports(
            no_of_clients,
            all_existing_ladspa_ports,
            dry_run=True,
        )
        == panning_positions
    )
