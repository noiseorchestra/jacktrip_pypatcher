from unittest.mock import Mock
import patcher_callback


def test_jacktrip_v1_2():
    assert patcher_callback.check_for_jacktrip_client("...ffff.123.123.123.123")


def test_jacktrip_v1_3():
    assert patcher_callback.check_for_jacktrip_client("__ffff.123.123.123.123")


def test_non_jacktrip_client():
    assert patcher_callback.check_for_jacktrip_client("00ffff.123.123.123.123") == False
