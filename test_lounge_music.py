from unittest.mock import Mock
from lounge_music import LoungeMusic


def test_start_the_music_with_retries():
    jackClient = Mock(spec=["get_ports"])
    jackClient.get_ports.return_value = []
    dry_run = True
    lounge_music = LoungeMusic(
        jackClient, "lounge-music", "/home/sam/lounge-music.mp3", dry_run
    )

    lounge_music.start_the_music_with_retries()
    assert jackClient.get_ports.call_count == 4
    # This is going to test the last set of parameters passed to the function
    jackClient.get_ports.assert_called_with("lounge-music.*")


def test_start_the_music_with_more_retries():
    jackClient = Mock(spec=["get_ports"])
    jackClient.get_ports.return_value = []
    dry_run = True
    lounge_music = LoungeMusic(
        jackClient, "lounge-music", "/home/sam/lounge-music.mp3", dry_run
    )

    lounge_music.start_the_music_with_retries(10)
    assert jackClient.get_ports.call_count == 11
    # This is going to test the last set of parameters passed to the function
    jackClient.get_ports.assert_called_with("lounge-music.*")
