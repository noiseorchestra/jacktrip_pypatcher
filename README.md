# Madwort Auto Patcher

Use [JackClient Python API](https://github.com/spatialaudio/jackclient-python/) to do some autopatching for our [JackTrip](https://github.com/jacktrip/jacktrip) server

## Install

To use this on Ubuntu 18, you'll need to install jackclient-python's dependencies, which currently means the following:

```bash
$ sudo aptitude install python3-pip
$ python3 -m pip install -r requirements.txt --user
```

### Services

Systemd service files are in `./services`, see the [README.md](./services/README.md) there.

## Usage

### hub server

The hub server will do its own autopatching, so disable all that by ensuring you're in hub autopatch mode 0 and set the `--nojackportsconnect` flag, e.g.

```bash
hubserver$ jacktrip -S -p0 --nojackportsconnect
```

You can also start this using the service definitions above!

### hard-coded paths

* Ensure that you have some lounge music path at the currently hard-coded path in [lounge_music.py](./lounge_music.py), currently `/home/sam/lounge-music.mp3`.

* Ensure that you have write access to the currently hard-coded path in [stereo_recording.py](./stereo_recording.py), currently `/home/sam/`. Nb. files will have filenames with prefix `darkice-`, e.g. `darkice-01.wav`.

### more stuff

Start the LADSPA plugins (if you are expecting more than 5 clients):

```bash
hubserver$ ./start_plugins.sh
```

Then re-run this script whenever a client connects/disconnects:

```bash
hubserver$ python3 jacktrip_pypatcher.py
```

### Modes

* `jacktrip_pypatcher_mode_2.py` should replicate what the built-in autopatcher does when in `-p2` mode
* `jacktrip_pypatcher.py` should do all the patching you ever need!

### Mono/Stereo clients

The default is that clients send a mono signal (arrives at the hubserver as `receive_1`), and receive a stereo mix (sent from the hubserver as `send_1,2`). These clients should be running jacktrip with `-n2`

#### Mono headphone mix

Some clients would prefer to receive a mono headphone mix, as they can then wear their headphones only on one ear & hear the acoustic sound in their room with their other ear. The easiest thing is for these clients to run jacktrip with `-n1`.

Alternatively they can patch `jacktrip/receive_2` to `system/playback_1` on their local jackd server.

#### Stereo signal

Clients that are sending a stereo signal (e.g. two musicians at one computer, electronic musicians generating stereo output) need to have their ip address added to the [list of stereo clients in the script](https://github.com/madwort/jacktrip_pypatcher/blob/a5e8b56b331f42fc9a2a6d40cce62dc41c9963a9/jacktrip_pypatcher.py#L254) before running the script.

#### Stereo signal and mono headphone mix

Clients should be enabled for stereo signal as above, but obviously they will not be able to run jacktrip with `-n1` so should patch their headphone mix in their local jackd server.

### LADSPA/Jack plugins

In order to use 5/6 clients, you'll need to have some panning plugins.

#### Install

```bash
$ sudo aptitude install invada-studio-plugins-ladspa
$ git clone https://repo.or.cz/ng-jackspa.git
$ sudo aptitude install libglib2.0-dev libncurses5-dev ladspa-sdk ladspa-sdk-dev
$ cd ng-jackspa
# trying to avoid building the GTK version...!
$ make njackspa jackspa-cli
$ ./njackspa /usr/lib/ladspa/inv_input.so 3301
```

For example:

```bash
tom@noiseaa1:~/ng-jackspa$ ./jackspa-cli -j right-50 -i '0:0:0:0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
tom@noiseaa1:~/ng-jackspa$ jack_lsp
system:capture_1
system:capture_2
system:playback_1
system:playback_2
right-50:Input (Left)
right-50:Input (Right)
right-50:Output (Left)
right-50:Output (Right)
```

#### Usage

To use this autopatcher, you'll need to run `start_plugins.sh` and `stop_plugins.sh` accordingly!

## Run tests

Run tests with:
```bash
$ python3 -m pytest
```

Nb. these currently "fail", but give useful output that you can use to verify what the script is attempting to do!

## Credits

Written by Tom Ward ( http://www.madwort.co.uk ) as part of a project with Noise Orchestra ( https://noiseorchestra.org/ )
