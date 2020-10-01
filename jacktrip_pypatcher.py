import jack
import time
import lounge_music
import stereo_recording
import jack_client_patching as p
import ladspa_plugins as ladspa


def disconnect(jackClient, dry_run, hold_music_port):
    """Disconnect all autopatched ports"""
    # TODO: only remove autopatched connections, not our own connections (HOW?)
    all_jacktrip_receive_ports = jackClient.get_ports(".*receive.*")
    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    all_hold_music_ports = jackClient.get_ports(hold_music_port + ".*")
    if dry_run:
        all_hold_music_ports = []

    jcp = p.JackClientPatching(jackClient, dry_run)

    # TODO: implement dry_run mode!
    for receive_port in all_jacktrip_receive_ports:
        jcp.disconnect_all(receive_port)

    for ladspa_port in all_ladspa_ports:
        jcp.disconnect_all(ladspa_port)

    for port in all_hold_music_ports:
        jcp.disconnect_all(port)


def connect_all(jcp, jacktrip_clients, ladspa_ports):
    """Connect all JackTrip clients to a list of ladspa ports"""
    for i, ladspa_port in enumerate(ladspa_ports):
        jcp.connect_to_ladspa(jacktrip_clients[i], ladspa_port)
        for jacktrip_client in jacktrip_clients:
            if jacktrip_client == jacktrip_clients[i]:
                continue
            else:
                jcp.connect_from_ladspa(ladspa_port, jacktrip_client)


def get_current_clients(jackClient, dry_run):
    """Get an array of client jack port prefixes"""
    return list(
        map(lambda x: x.name.split(":")[0], jackClient.get_ports(".*receive_1"))
    )


def verify_ladspa_plugins(jackClient):
    """Verify that the LADSPA plugins are running and abort if not"""
    all_left_ladspa_ports = jackClient.get_ports("ladspa-left-.*")
    if len(all_left_ladspa_ports) < 1:
        print("Start LADSPA plugins please!")
        # TODO: verify SystemExit is working as intended
        SystemExit(1)


def get_darkice_port(jackClient, dry_run, darkice_prefix):
    """Get the current darkice jack port prefix"""
    darkice_ports = list(
        map(
            lambda x: x.name.split(":")[0],
            jackClient.get_ports(darkice_prefix + ".*:left"),
        )
    )

    if dry_run:
        darkice_ports = ["darkice-10545"]

    if len(darkice_ports) == 0:
        print("Start darkice first, please")
        SystemExit(1)

    return darkice_ports[0]


def autopatch(jackClient, dry_run, jacktrip_clients):
    """Autopatch all the things!"""

    print("=== Clients ===")
    print("client count:", len(jacktrip_clients))
    print("clients", jacktrip_clients)

    hold_music_port = "lounge-music"
    darkice_prefix = "darkice"

    all_panning_positions = [0, -0.15, 0.15, -0.3, 0.3, -0.45,
                             0.45, -0.6, 0.6, -0.75, 0.75]

    print("=== Disconnecting existing connections ===")
    disconnect(jackClient, dry_run, hold_music_port)

    print("=== Start LADSPA plugins ===")

    all_ladspa_ports = jackClient.get_ports("ladspa-.*")
    print("Current ladspa ports: ", len(all_ladspa_ports))

    if len(jacktrip_clients) <= 1 and len(all_ladspa_ports) > 0:
        ladspa.kill_plugins(jackClient)

    print("=== Creating new connections ===")

    darkice_port = get_darkice_port(jackClient, dry_run, darkice_prefix)
    print("darkice port:", darkice_port)

    jcp = p.JackClientPatching(jackClient, dry_run)

    max_supported_clients = 11
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
        lounge_music.kill_the_music(jackClient, hold_music_port)
        SystemExit(1)

    if len(jacktrip_clients) == 1:
        # start hold music & patch to the one client
        lounge_music.start_the_music(jackClient, hold_music_port)

        all_hold_music_ports = jackClient.get_ports(hold_music_port + ".*")
        if len(all_hold_music_ports) == 0:
            # this is a crude fix because mpg123 wasn't always starting
            # expect we won't need this with the server upgrade as audio
            # processing is much less error prone
            count = 0
            while count < 3:
                lounge_music.start_the_music(jackClient, hold_music_port)
                count += 1
                time.sleep(0.5)

        jcp.connect_mpg123_to_centre(hold_music_port, jacktrip_clients[0])

        # also connect loopback
        jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[0])

        print("-- darkice --")
        jcp.connect_mpg123_to_darkice(hold_music_port, darkice_port)
        jcp.connect_darkice_to_centre(jacktrip_clients[0], darkice_port)

    if len(jacktrip_clients) == 2:

        jcp.connect_to_centre(jacktrip_clients[1], jacktrip_clients[0])
        jcp.connect_to_centre(jacktrip_clients[0], jacktrip_clients[1])

        print("-- darkice --")
        jcp.connect_to_ladspa(jacktrip_clients[0], ladspa.get_port(jackClient, all_panning_positions[5]))
        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa.get_port(jackClient, all_panning_positions[6]))

        jcp.connect_darkice_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[5]), darkice_port)
        jcp.connect_darkice_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[6]), darkice_port)

    if len(jacktrip_clients) == 3:
        # Connections for 3 clients are a bit special as we need to make sure the L-R
        # balance for each client is even (not two peers in one channel)

        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa.get_port(jackClient, all_panning_positions[3]))
        jcp.connect_to_ladspa(jacktrip_clients[2], ladspa.get_port(jackClient, all_panning_positions[4]))

        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[3]), jacktrip_clients[0])
        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[4]), jacktrip_clients[0])

        jcp.connect_to_ladspa(jacktrip_clients[0], ladspa.get_port(jackClient, all_panning_positions[5]))
        jcp.connect_to_ladspa(jacktrip_clients[2], ladspa.get_port(jackClient, all_panning_positions[6]))

        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[5]), jacktrip_clients[1])
        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[6]), jacktrip_clients[1])

        jcp.connect_to_ladspa(jacktrip_clients[0], ladspa.get_port(jackClient, all_panning_positions[7]))
        jcp.connect_to_ladspa(jacktrip_clients[1], ladspa.get_port(jackClient, all_panning_positions[8]))

        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[7]), jacktrip_clients[2])
        jcp.connect_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[8]), jacktrip_clients[2])

        print("-- darkice --")

        jcp.connect_darkice_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[5]), darkice_port)
        jcp.connect_darkice_from_ladspa(ladspa.get_port(jackClient, all_panning_positions[6]), darkice_port)
        jcp.connect_darkice_to_centre(jacktrip_clients[1], darkice_port)

    if len(jacktrip_clients) >= 4 and len(jacktrip_clients) <= 11:
        ladspa_ports = ladspa.get_ports(len(jacktrip_clients), all_panning_positions)
        connect_all(jcp, jacktrip_clients, ladspa_ports)

        print("-- darkice --")
        for ladspa_port in ladspa_ports:
            jcp.connect_darkice_from_ladspa(ladspa_port, darkice_port)

    if len(jacktrip_clients) > 11:
        print("Not yet implemented")
        SystemExit(1)

def main(dry_run=True):
    """Do some setup, then do the autopatch"""
    jackClient = jack.Client("MadwortAutoPatcher")

    jacktrip_clients = get_current_clients(jackClient, dry_run)

    autopatch(jackClient, dry_run, jacktrip_clients)

    jackClient.deactivate()
    jackClient.close()


if __name__ == "__main__":
    main()
