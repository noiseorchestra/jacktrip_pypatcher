import jack
import jacktrip_pypatcher

def run_pypatcher_voice_count(number_of_voices):
  jackClient = jack.Client('TestAutoPatcher')
  dry_run = True

  jacktrip_clients = ['..ffff.192.168.0.1', '..ffff.192.168.0.2',
                      '..ffff.192.168.0.3', '..ffff.192.168.0.4',
                      '..ffff.192.168.0.5', '..ffff.192.168.0.6']
  jacktrip_clients = jacktrip_clients[0:number_of_voices]

  jacktrip_stereo = jacktrip_clients[0:1]
  jacktrip_clients_stereo = list(map(lambda x: x in jacktrip_stereo, jacktrip_clients))

  # TODO: hacky way to use pytest - we know this assertion will fail, but at the moment
  # we can just inspect the stdout
  assert jacktrip_pypatcher.autopatch(jackClient, dry_run, jacktrip_clients, jacktrip_clients_stereo) == True

# TODO: when we have actual tests, we can use a loop here
def test_pypatcher2():
  run_pypatcher_voice_count(2)

def test_pypatcher6():
  run_pypatcher_voice_count(6)
