import jack
from stereo_recording import StereoRecording
import jack_client_patching as p
from ladspa_plugins import LadspaPlugins
from lounge_music import LoungeMusic
from darkice import Darkice


def disconnect(jackClient, dry_run, lounge_music_port):
    """Disconnect all autopatched ports"""
    # TODO: only remove autopatched connections, not our own connections (HOW?)
    all_jacktrip_receive_ports = jackClient.get_ports(".*receive.*")
    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    all_lounge_music_ports = jackClient.get_ports(lounge_music_port + ".*")
    if dry_run:
        all_lounge_music_ports = []

    jcp = p.JackClientPatching(jackClient, dry_run)

    for receive_port in all_jacktrip_receive_ports:
        jcp.disconnect_all(receive_port)

    for ladspa_port in all_ladspa_ports:
        jcp.disconnect_all(ladspa_port)

    for port in all_lounge_music_ports:
        jcp.disconnect_all(port)


def get_current_clients(jackClient, dry_run):
    """Get an array of client jack port prefixes"""
    return list(
        map(lambda x: x.name.split(":")[0], jackClient.get_ports(".*receive_1"))
    )


def autopatch(jackClient, dry_run, jacktrip_clients):
    """Autopatch all the things!"""

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
    jackspa_path = "/home/sam/ng-jackspa/jackspa-cli"
    lounge_music_path = "/home/sam/lounge-music.mp3"
    recording_path_prefix = "/home/sam/darkice-"

    lounge_music = LoungeMusic(jackClient, "lounge-music", lounge_music_path, dry_run)
    stereo_recording = StereoRecording(recording_path_prefix, dry_run)
    darkice = Darkice(jackClient, "darkice", dry_run)
    ladspa = LadspaPlugins(jackClient, jackspa_path, all_panning_positions, dry_run)
    jcp = p.JackClientPatching(jackClient, dry_run)

    print("=== JackTrip clients ===")
    print("client count:", len(jacktrip_clients))
    print("clients:", jacktrip_clients)

    max_supported_clients = len(ladspa.all_positions)
    if len(jacktrip_clients) > max_supported_clients:
        print(
            "Unsupported number of clients, patching",
            max_supported_clients,
            "of",
            len(jacktrip_clients),
        )
        jacktrip_clients = jacktrip_clients[0:max_supported_clients]

    print("=== LADSPA ports ===")
    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    print("Current ladspa plugins:", len(all_ladspa_ports))
    print("ports:", all_ladspa_ports)

    if len(jacktrip_clients) <= 1 and len(all_ladspa_ports) > 0:
        print("Killing LADSPA plugins")
        ladspa.kill_plugins()
        all_ladspa_ports = jackClient.get_ports("ladspa-.*")
        print("Current ladspa plugins:", len(all_ladspa_ports))

    print("=== Darkice ===")
    darkice_port = darkice.get_port()
    print("darkice port:", darkice_port)

    print("=== Disconnecting existing connections ===")
    disconnect(jackClient, dry_run, lounge_music.port)

    print("=== Lounge Music ===")
    if len(jacktrip_clients) != 1:
        lounge_music.kill_the_music()
    else:
        lounge_music.start_the_music_with_retries()

    if len(jacktrip_clients) >= 1 and len(jacktrip_clients) <= 11:
        print("=== Start LADSPA plugins ===")
        ladspa_ports = ladspa.get_ports(len(jacktrip_clients), all_ladspa_ports)
        darkice_ladspa_ports = ladspa_ports
        if len(jacktrip_clients) == 3:
            darkice_ladspa_ports = [ladspa_ports[0]] + ladspa_ports[3:]

        jcp.set_all_connections(jacktrip_clients, ladspa_ports, lounge_music.port)
        jcp.set_darkice_connections(
            darkice_ladspa_ports, darkice_port, jacktrip_clients, lounge_music.port
        )

        print("=== Patch", len(jacktrip_clients), "client ===")
        jcp.make_all_connections()

    print("=== Recording ===")
    if len(jacktrip_clients) > 0:
        stereo_recording.start()
    else:
        stereo_recording.stop()


def main(dry_run=False):
    """Do some setup, then do the autopatch"""
    jackClient = jack.Client("MadwortAutoPatcher")
    jacktrip_clients = get_current_clients(jackClient, dry_run)
    autopatch(jackClient, dry_run, jacktrip_clients)
    jackClient.deactivate()
    jackClient.close()


if __name__ == "__main__":
    main()
