import jack
import jacktrip_pypatcher

def test_pypatcher():
  jackClient = jack.Client('TestAutoPatcher')
  assert jacktrip_pypatcher.get_current_clients(jackClient, True, 3)[0] == '..ffff.192.168.0.1'
