import jack_client_patching as p


def test_set_jacktrip_connections_1_client():

    jackClient = None
    jacktrip_clients = [
        "..ffff.192.168.0.1",
    ]

    connections = [
        ("..ffff.192.168.0.1:receive_.*", "..ffff.192.168.0.1:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, [])

    assert jcp.connections == connections


def test_set_darkice_connections_1_clients():

    jackClient = None
    jacktrip_clients = ["..ffff.192.168.0.1"]
    darkice_port = "darkice"

    connections = [
        ("..ffff.192.168.0.1:receive_.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_darkice_connections([], darkice_port, jacktrip_clients)

    assert jcp.connections == connections


def test_set_lounge_music_connections_1_clients():

    jackClient = None
    jacktrip_clients = ["..ffff.192.168.0.1"]
    darkice_port = "darkice"
    lounge_music_port = "lounge-music"

    connections = [
        ("lounge-music.*", "darkice.*"),
        ("lounge-music.*", "..ffff.192.168.0.1:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_lounge_music_connections(jacktrip_clients, darkice_port, lounge_music_port)

    assert jcp.connections == connections


def run_set_jacktrip_connections_2_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
    ]
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
    ]

    connections = [
        (
            client_prefix + "ffff.192.168.0.1:receive_.*",
            client_prefix + "ffff.192.168.0.2:send_.*",
        ),
        (
            client_prefix + "ffff.192.168.0.2:receive_.*",
            client_prefix + "ffff.192.168.0.1:send_.*",
        ),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-right-45:Input.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def run_set_darkice_connections_2_clients():

    jackClient = None
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
    ]

    darkice_port = "darkice"

    connections = [
        ("ladspa-left-45:Output.*", "darkice.*"),
        ("ladspa-right-45:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def run_set_client_connections_2_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
    ]
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
    ]

    darkice_port = "darkice"

    connections = [
        (
            client_prefix + "ffff.192.168.0.1:receive_.*",
            client_prefix + "ffff.192.168.0.2:send_.*",
        ),
        (
            client_prefix + "ffff.192.168.0.2:receive_.*",
            client_prefix + "ffff.192.168.0.1:send_.*",
        ),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-right-45:Input.*"),
        ("ladspa-left-45:Output.*", "darkice.*"),
        ("ladspa-right-45:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def run_set_jacktrip_connections_4_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
        client_prefix + "ffff.192.168.0.3",
        client_prefix + "ffff.192.168.0.4",
    ]
    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    connections = [
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-30:Input.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-right-30:Input.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.3:receive_.*", "ladspa-left-60:Input.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.4:receive_.*", "ladspa-right-60:Input.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def run_set_darkice_connections_4_clients():

    jackClient = None

    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    darkice_port = "darkice"

    connections = [
        ("ladspa-left-30:Output.*", "darkice.*"),
        ("ladspa-right-30:Output.*", "darkice.*"),
        ("ladspa-left-60:Output.*", "darkice.*"),
        ("ladspa-right-60:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def run_set_client_connections_4_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
        client_prefix + "ffff.192.168.0.3",
        client_prefix + "ffff.192.168.0.4",
    ]
    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    darkice_port = "darkice"

    connections = [
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-30:Input.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-right-30:Input.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-right-30:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.3:receive_.*", "ladspa-left-60:Input.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-60:Output.*", client_prefix + "ffff.192.168.0.4:send_.*"),
        (client_prefix + "ffff.192.168.0.4:receive_.*", "ladspa-right-60:Input.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-right-60:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "darkice.*"),
        ("ladspa-right-30:Output.*", "darkice.*"),
        ("ladspa-left-60:Output.*", "darkice.*"),
        ("ladspa-right-60:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def run_set_jacktrip_connections_3_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
        client_prefix + "ffff.192.168.0.3",
    ]
    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    connections = [
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-centre:Input.*"),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-right-45:Input.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-left-46:Input.*"),
        (client_prefix + "ffff.192.168.0.3:receive_.*", "ladspa-right-46:Input.*"),
        ("ladspa-left-46:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-46:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-left-45:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-right-46:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-46:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-right-45:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def run_set_darkice_connections_3_clients():

    jackClient = None
    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    darkice_port = "darkice"

    connections = [
        ("ladspa-centre:Output.*", "darkice.*"),
        ("ladspa-left-46:Output.*", "darkice.*"),
        ("ladspa-right-46:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_darkice_connections([ladspa_ports[0]] + ladspa_ports[3:], darkice_port)

    assert jcp.connections == connections


def run_set_client_connections_3_clients(client_prefix):

    jackClient = None
    jacktrip_clients = [
        client_prefix + "ffff.192.168.0.1",
        client_prefix + "ffff.192.168.0.2",
        client_prefix + "ffff.192.168.0.3",
    ]
    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    ladspa_ports = [
        "ladspa-centre",
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    darkice_port = "darkice"

    connections = [
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-centre:Input.*"),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        (client_prefix + "ffff.192.168.0.1:receive_.*", "ladspa-right-45:Input.*"),
        (client_prefix + "ffff.192.168.0.2:receive_.*", "ladspa-left-46:Input.*"),
        (client_prefix + "ffff.192.168.0.3:receive_.*", "ladspa-right-46:Input.*"),
        ("ladspa-left-46:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-right-46:Output.*", client_prefix + "ffff.192.168.0.1:send_.*"),
        ("ladspa-left-45:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-right-46:Output.*", client_prefix + "ffff.192.168.0.2:send_.*"),
        ("ladspa-left-46:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-right-45:Output.*", client_prefix + "ffff.192.168.0.3:send_.*"),
        ("ladspa-centre:Output.*", "darkice.*"),
        ("ladspa-left-46:Output.*", "darkice.*"),
        ("ladspa-right-46:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_client_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections([ladspa_ports[0]] + ladspa_ports[3:], darkice_port)

    assert jcp.connections == connections


client_prefixes = ["..", "__"]


def test_jacktrip_connections():
    for client_prefix in client_prefixes:
        print(client_prefix)
        run_set_jacktrip_connections_2_clients(client_prefix)
        run_set_jacktrip_connections_3_clients(client_prefix)
        run_set_jacktrip_connections_4_clients(client_prefix)


def test_darkice_connections():
    run_set_darkice_connections_2_clients()
    run_set_darkice_connections_3_clients()
    run_set_darkice_connections_4_clients()


def test_all_connections():
    for client_prefix in client_prefixes:
        run_set_client_connections_2_clients(client_prefix)
        run_set_client_connections_3_clients(client_prefix)
        run_set_client_connections_4_clients(client_prefix)
