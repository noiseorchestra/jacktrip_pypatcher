import jacktrip_pypatcher
import ladspa_plugins as ladspa
from unittest.mock import Mock


def run_pypatcher_voice_count(number_of_voices, expected_call_count=4):
    jackClient = Mock(spec=["get_ports"])
    # We need to mock this in this way because we're going to split the name string
    mockPort = Mock()
    mockPort.name = "mockport:1"
    ladspa_ports = []
    jackClient.get_ports.return_value = [mockPort]
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

    # Nb. this won't test the logic of the patching, but may be useful as some kind
    # of integration test to check for other issues
    jacktrip_pypatcher.autopatch(jackClient, dry_run, jacktrip_clients)
    assert jackClient.get_ports.call_count == expected_call_count
    # This is going to test the last set of parameters passed to the function
    jackClient.get_ports.assert_called_with("lounge-music.*")


# TODO: when we have actual tests, we can use a loop here
def test_pypatcher1():
    # different get_ports call count expected because of lounge_music being started
    # and ladspa being shut down. This is still a hack but can be fixed in a full
    # rewrite of these tests.
    run_pypatcher_voice_count(1, expected_call_count=6)


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
