import jack
import time
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

    print("=== Clients ===")
    print("client count:", len(jacktrip_clients))
    print("clients", jacktrip_clients)

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

    lounge_music = LoungeMusic(
        jackClient, "lounge-music", "/home/sam/lounge-music.mp3", dry_run
    )
    stereo_recording = StereoRecording("/home/sam/darkice-", dry_run)
    darkice = Darkice(jackClient, "darkice", dry_run)
    ladspa = LadspaPlugins(
        jackClient, "/home/sam/ng-jackspa/jackspa-cli", all_panning_positions, dry_run
    )

    print("=== Disconnecting existing connections ===")
    disconnect(jackClient, dry_run, lounge_music.port)

    print("=== Start LADSPA plugins ===")

    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    print("Current ladspa ports: ", len(all_ladspa_ports))

    if len(jacktrip_clients) <= 1 and len(all_ladspa_ports) > 0:
        ladspa.kill_plugins()

    print("=== Creating new connections ===")

    darkice_port = darkice.get_port()
    print("darkice port:", darkice_port)

    jcp = p.JackClientPatching(jackClient, dry_run)

    max_supported_clients = len(ladspa.all_positions)
    if len(jacktrip_clients) > max_supported_clients:
        print(
            "Unsupported number of clients, patching",
            max_supported_clients,
            "of",
            len(jacktrip_clients),
        )
        jacktrip_clients = jacktrip_clients[0:max_supported_clients]

    if len(jacktrip_clients) > 0:
        stereo_recording.start()
    else:
        stereo_recording.stop()

    if len(jacktrip_clients) != 1:
        # Only play the hold music if there is exactly one person connected!
        lounge_music.kill_the_music()
        SystemExit(1)

    if len(jacktrip_clients) == 1:
        # start hold music & patch to the one client
        lounge_music.start_the_music_with_retries()

        jcp.connect_mpg123_to_centre(lounge_music.port, jacktrip_clients[0])

        # also connect loopback
        jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[0])

        print("-- darkice --")
        jcp.connect_mpg123_to_darkice(lounge_music.port, darkice_port)
        jcp.connect_darkice_to_centre(jacktrip_clients[0], darkice_port)

    if len(jacktrip_clients) == 2 or len(jacktrip_clients) == 3:

        panning_positions = ladspa.get_panning_positions(len(jacktrip_clients))

        # ports needed for 2 & 3 client sessions
        # if we like this method we can add the positions to all_panning_positions
        ladspa_mid_left_1 = ladspa.get_port(panning_positions[0], all_ladspa_ports)
        ladspa_mid_right_1 = ladspa.get_port(panning_positions[1], all_ladspa_ports)
        ladspa_mid_left_2 = ladspa.get_port(panning_positions[2], all_ladspa_ports)
        ladspa_mid_right_2 = ladspa.get_port(panning_positions[3], all_ladspa_ports)

    if len(jacktrip_clients) == 2:

        jcp.connect_to_centre(jacktrip_clients[1], jacktrip_clients[0])
        jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[1])

        print("-- darkice --")
        jcp.connect_to_ladspa(jacktrip_clients[0], ladspa_mid_left_1)
        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_mid_right_2)

        jcp.connect_darkice_from_ladspa(ladspa_mid_left_1, darkice_port)
        jcp.connect_darkice_from_ladspa(ladspa_mid_right_2, darkice_port)

    if len(jacktrip_clients) == 3:
        # Connections for 3 clients are a bit special as we need to make sure the L-R
        # balance for each client is even (not two peers in one channel)

        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_mid_left_1)
        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa_mid_right_1)
        jcp.connect_to_ladspa(jacktrip_clients[0], ladspa_mid_left_2)
        jcp.connect_to_ladspa(jacktrip_clients[2], ladspa_mid_right_2)

        jcp.connect_from_ladspa(ladspa_mid_left_1, jacktrip_clients[0])
        jcp.connect_from_ladspa(ladspa_mid_right_2, jacktrip_clients[0])

        jcp.connect_from_ladspa(ladspa_mid_left_2, jacktrip_clients[1])
        jcp.connect_from_ladspa(ladspa_mid_right_2, jacktrip_clients[1])

        jcp.connect_from_ladspa(ladspa_mid_left_2, jacktrip_clients[2])
        jcp.connect_from_ladspa(ladspa_mid_right_1, jacktrip_clients[2])

        print("-- darkice --")

        jcp.connect_darkice_from_ladspa(ladspa_mid_left_2, darkice_port)
        jcp.connect_darkice_from_ladspa(ladspa_mid_right_2, darkice_port)
        jcp.connect_darkice_to_centre(jacktrip_clients[1], darkice_port)

    if len(jacktrip_clients) >= 4 and len(jacktrip_clients) <= 11:
        ladspa_ports = ladspa.get_ports(len(jacktrip_clients), all_ladspa_ports)
        jcp.set_all_connections(jacktrip_clients, ladspa_ports)
        jcp.make_all_connections()

        print("-- darkice --")
        for ladspa_port in ladspa_ports:
            jcp.connect_darkice_from_ladspa(ladspa_port, darkice_port)

    if len(jacktrip_clients) > 11:
        print("Not yet implemented")
        SystemExit(1)


def main(dry_run=False):
    """Do some setup, then do the autopatch"""
    jackClient = jack.Client("MadwortAutoPatcher")

    jacktrip_clients = get_current_clients(jackClient, dry_run)

    autopatch(jackClient, dry_run, jacktrip_clients)

    jackClient.deactivate()
    jackClient.close()


if __name__ == "__main__":
    main()
