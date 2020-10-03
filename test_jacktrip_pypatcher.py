import jack
import jacktrip_pypatcher
import ladspa_plugins as ladspa

def test_generate_subprocess_cmd(position=0.3):

    cmd = ["/home/sam/ng-jackspa/jackspa-cli",
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
    port_names = ["ladspa-centre",
                  "ladspa-left-30",
                  "ladspa-right-30",
                  "ladspa-left-60",
                  "ladspa-right-60"]

    assert [ladspa.generate_port_name(position) for position in panning_positions] == port_names

# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_and_check_port():

    class LadspaClient:
        def __init__(self, name):
            self.name = name

    jackClient = None
    dry_run=True
    panning_positions = [0, -0.3, 0.3, -0.6, 0.6]
    all_existing_ladspa_ports = [LadspaClient("ladspa-centre")]

    result = ["ladspa-centre",
              "ladspa-left-30",
              "ladspa-right-30",
              "ladspa-left-60",
              "ladspa-right-60"]

    assert [ladspa.get_port(jackClient, position, all_existing_ladspa_ports, dry_run=True) for position in panning_positions] == result

# run pytest with -rP flag to see stdout logs showing which ports need to be started
def test_get_ports():

    class LadspaClient:
        def __init__(self, name):
            self.name = name

    jackClient = None
    dry_run=True
    all_panning_positions = [0, -0.15, 0.15, -0.3, 0.3, -0.45,
                             0.45, -0.6, 0.6, -0.75, 0.75]
    no_of_clients = 4
    all_existing_ladspa_ports = [LadspaClient("ladspa-centre")]
    panning_positions = [ladspa.generate_port_name(position) for position in all_panning_positions[3:7]]

    assert ladspa.get_ports(jackClient, no_of_clients, all_panning_positions, all_existing_ladspa_ports, dry_run) == panning_positions


def run_pypatcher_voice_count(number_of_voices):
    jackClient = jack.Client("TestAutoPatcher")
    dry_run = True

    jacktrip_clients = [
        "..ffff.192.168.0.1",
        "..ffff.192.168.0.2",
        "..ffff.192.168.0.3",
        "..ffff.192.168.0.4",
        "..ffff.192.168.0.5",
        "..ffff.192.168.0.6",
        "..ffff.192.168.0.7",
        "..ffff.192.168.0.8",
        "..ffff.192.168.0.9",
        "..ffff.192.168.0.10",
        "..ffff.192.168.0.11",
        "..ffff.192.168.0.12",
    ]
    jacktrip_clients = jacktrip_clients[0:number_of_voices]

    # TODO: hacky way to use pytest - we know this assertion will fail, but at the moment
    # we can just inspect the stdout
    assert jacktrip_pypatcher.autopatch(jackClient, dry_run, jacktrip_clients) == True


# TODO: when we have actual tests, we can use a loop here
def test_pypatcher2():
    run_pypatcher_voice_count(2)


def test_pypatcher6():
    run_pypatcher_voice_count(6)


def test_pypatcher7():
    run_pypatcher_voice_count(7)


def test_pypatcher8():
    run_pypatcher_voice_count(8)


def test_pypatcher11():
    run_pypatcher_voice_count(11)
