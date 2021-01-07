import jack_client_patching as p


def test_set_jacktrip_connections_2_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
    ]
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
    ]

    connections = [
        ("__ffff.192.168.0.1:receive_.*", "__ffff.192.168.0.2:send_.*"),
        ("__ffff.192.168.0.2:receive_.*", "__ffff.192.168.0.1:send_.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-right-45:Input.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def test_set_darkice_connections_2_clients():

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


def test_set_all_connections_2_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
    ]
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
    ]

    darkice_port = "darkice"

    connections = [
        ("__ffff.192.168.0.1:receive_.*", "__ffff.192.168.0.2:send_.*"),
        ("__ffff.192.168.0.2:receive_.*", "__ffff.192.168.0.1:send_.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-right-45:Input.*"),
        ("ladspa-left-45:Output.*", "darkice.*"),
        ("ladspa-right-45:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def test_set_jacktrip_connections_4_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
        "__ffff.192.168.0.3",
        "__ffff.192.168.0.4",
    ]
    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    connections = [
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-30:Input.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-right-30:Input.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.3:receive_.*", "ladspa-left-60:Input.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.4:receive_.*", "ladspa-right-60:Input.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.3:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def test_set_darkice_connections_4_clients():

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


def test_set_all_connections_4_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
        "__ffff.192.168.0.3",
        "__ffff.192.168.0.4",
    ]
    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    darkice_port = "darkice"

    connections = [
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-30:Input.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-right-30:Input.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-right-30:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.3:receive_.*", "ladspa-left-60:Input.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-60:Output.*", "__ffff.192.168.0.4:send_.*"),
        ("__ffff.192.168.0.4:receive_.*", "ladspa-right-60:Input.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-right-60:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "darkice.*"),
        ("ladspa-right-30:Output.*", "darkice.*"),
        ("ladspa-left-60:Output.*", "darkice.*"),
        ("ladspa-right-60:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections


def test_set_jacktrip_connections_3_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
        "__ffff.192.168.0.3",
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
        ("__ffff.192.168.0.1:receive_.*", "ladspa-centre:Input.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-right-45:Input.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-left-46:Input.*"),
        ("__ffff.192.168.0.3:receive_.*", "ladspa-right-46:Input.*"),
        ("ladspa-left-46:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-46:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-left-45:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-right-46:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-46:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-right-45:Output.*", "__ffff.192.168.0.3:send_.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections == connections


def test_set_darkice_connections_3_clients():

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


def test_set_all_connections_3_clients():

    jackClient = None
    jacktrip_clients = [
        "__ffff.192.168.0.1",
        "__ffff.192.168.0.2",
        "__ffff.192.168.0.3",
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
        ("__ffff.192.168.0.1:receive_.*", "ladspa-centre:Input.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-left-45:Input.*"),
        ("__ffff.192.168.0.1:receive_.*", "ladspa-right-45:Input.*"),
        ("__ffff.192.168.0.2:receive_.*", "ladspa-left-46:Input.*"),
        ("__ffff.192.168.0.3:receive_.*", "ladspa-right-46:Input.*"),
        ("ladspa-left-46:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-right-46:Output.*", "__ffff.192.168.0.1:send_.*"),
        ("ladspa-left-45:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-right-46:Output.*", "__ffff.192.168.0.2:send_.*"),
        ("ladspa-left-46:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-right-45:Output.*", "__ffff.192.168.0.3:send_.*"),
        ("ladspa-centre:Output.*", "darkice.*"),
        ("ladspa-left-46:Output.*", "darkice.*"),
        ("ladspa-right-46:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections([ladspa_ports[0]] + ladspa_ports[3:], darkice_port)

    assert jcp.connections == connections
