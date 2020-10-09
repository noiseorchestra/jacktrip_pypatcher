import jack_client_patching as p


def test_get_receive_string():
    jackClient = None
    jcp = p.JackClientPatching(jackClient, dry_run=True)

    jacktrip_receive = jcp.get_receive_string("..ffff.192.168.0.1", "jacktrip")
    ladspa_receive = jcp.get_receive_string("ladspa-left-30", "ladspa")
    darkice_receive = jcp.get_receive_string("lounge-music", "mpg123")

    assert jacktrip_receive == "..ffff.192.168.0.1:receive_.*"
    assert ladspa_receive == "ladspa-left-30:Output.*"
    assert darkice_receive == "lounge-music:.*"


def test_get_send_string():
    jackClient = None
    jcp = p.JackClientPatching(jackClient, dry_run=True)

    jacktrip_send = jcp.get_send_string("..ffff.192.168.0.1", "jacktrip")
    ladspa_send = jcp.get_send_string("ladspa-left-30", "ladspa")
    darkice_send = jcp.get_send_string("darkice", "darkice")

    assert jacktrip_send == "..ffff.192.168.0.1:send_.*"
    assert ladspa_send == "ladspa-left-30:Input.*"
    assert darkice_send == "darkice:.*"


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
