import jack_client_patching as p


def test_connections():

    jackClient = None
    jacktrip_clients = [
        "..ffff.192.168.0.1",
        "..ffff.192.168.0.2",
        "..ffff.192.168.0.3",
        "..ffff.192.168.0.4",
    ]
    ladspa_ports = [
        "ladspa-left-30",
        "ladspa-right-30",
        "ladspa-left-60",
        "ladspa-right-60",
    ]

    darkice_port = "darkice"

    connections = [
        ("..ffff.192.168.0.1:receive_.*", "ladspa-left-30:Input.*"),
        ("ladspa-left-30:Output.*", "..ffff.192.168.0.2:send_.*"),
        ("ladspa-left-30:Output.*", "..ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "..ffff.192.168.0.4:send_.*"),
        ("..ffff.192.168.0.2:receive_.*", "ladspa-right-30:Input.*"),
        ("ladspa-right-30:Output.*", "..ffff.192.168.0.1:send_.*"),
        ("ladspa-right-30:Output.*", "..ffff.192.168.0.3:send_.*"),
        ("ladspa-right-30:Output.*", "..ffff.192.168.0.4:send_.*"),
        ("..ffff.192.168.0.3:receive_.*", "ladspa-left-60:Input.*"),
        ("ladspa-left-60:Output.*", "..ffff.192.168.0.1:send_.*"),
        ("ladspa-left-60:Output.*", "..ffff.192.168.0.2:send_.*"),
        ("ladspa-left-60:Output.*", "..ffff.192.168.0.4:send_.*"),
        ("..ffff.192.168.0.4:receive_.*", "ladspa-right-60:Input.*"),
        ("ladspa-right-60:Output.*", "..ffff.192.168.0.1:send_.*"),
        ("ladspa-right-60:Output.*", "..ffff.192.168.0.2:send_.*"),
        ("ladspa-right-60:Output.*", "..ffff.192.168.0.3:send_.*"),
        ("ladspa-left-30:Output.*", "darkice.*"),
        ("ladspa-right-30:Output.*", "darkice.*"),
        ("ladspa-left-60:Output.*", "darkice.*"),
        ("ladspa-right-60:Output.*", "darkice.*"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)
    jcp.set_darkice_connections(ladspa_ports, darkice_port)

    assert jcp.connections == connections
