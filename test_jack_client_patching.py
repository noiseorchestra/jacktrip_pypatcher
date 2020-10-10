import jack_client_patching as p


def test_set_all_connections():

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

    connections_to_ladspa = [
        ("..ffff.192.168.0.1", "ladspa-left-30"),
        ("..ffff.192.168.0.2", "ladspa-right-30"),
        ("..ffff.192.168.0.3", "ladspa-left-60"),
        ("..ffff.192.168.0.4", "ladspa-right-60"),
    ]

    connections_from_ladspa = [
        ("ladspa-left-30", "..ffff.192.168.0.2"),
        ("ladspa-left-30", "..ffff.192.168.0.3"),
        ("ladspa-left-30", "..ffff.192.168.0.4"),
        ("ladspa-right-30", "..ffff.192.168.0.1"),
        ("ladspa-right-30", "..ffff.192.168.0.3"),
        ("ladspa-right-30", "..ffff.192.168.0.4"),
        ("ladspa-left-60", "..ffff.192.168.0.1"),
        ("ladspa-left-60", "..ffff.192.168.0.2"),
        ("ladspa-left-60", "..ffff.192.168.0.4"),
        ("ladspa-right-60", "..ffff.192.168.0.1"),
        ("ladspa-right-60", "..ffff.192.168.0.2"),
        ("ladspa-right-60", "..ffff.192.168.0.3"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections_to_ladspa == connections_to_ladspa
    assert jcp.connections_from_ladspa == connections_from_ladspa


def test_set_all_connections_3_clients():
    pytest.xfail("This configuration not currently supported")

    jackClient = None
    jacktrip_clients = [
        "..ffff.192.168.0.1",
        "..ffff.192.168.0.2",
        "..ffff.192.168.0.3",
    ]
    ladspa_ports = [
        "ladspa-left-45",
        "ladspa-right-45",
        "ladspa-left-46",
        "ladspa-right-46",
    ]

    connections_to_ladspa = [
        ("..ffff.192.168.0.1", "ladspa-left-45"),
        ("..ffff.192.168.0.2", "ladspa-left-46"),
        ("..ffff.192.168.0.2", "ladspa-right-46"),
        ("..ffff.192.168.0.3", "ladspa-right-45"),
    ]

    connections_from_ladspa = [
        ("ladspa-left-46", "..ffff.192.168.0.1"),
        ("ladspa-right-45", "..ffff.192.168.0.1"),
        ("ladspa-left-45", "..ffff.192.168.0.2"),
        ("ladspa-right-45", "..ffff.192.168.0.2"),
        ("ladspa-left-45", "..ffff.192.168.0.3"),
        ("ladspa-right-46", "..ffff.192.168.0.3"),
    ]

    jcp = p.JackClientPatching(jackClient, dry_run=True)
    jcp.set_all_connections(jacktrip_clients, ladspa_ports)

    assert jcp.connections_to_ladspa == connections_to_ladspa
    assert jcp.connections_from_ladspa == connections_from_ladspa
