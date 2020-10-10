# Madwort Auto Patcher

Use [JackClient Python API](https://github.com/spatialaudio/jackclient-python/) to do some autopatching for our [JackTrip](https://github.com/jacktrip/jacktrip) server

## Install

## Dependencies

- [JACK](https://jackaudio.org/)
- [jacktrip](https://github.com/jacktrip/jacktrip)
- [LADSPA/Jack plugins](https://repo.or.cz/ng-jackspa.git)
- [Icecast](https://github.com/xiph/Icecast-Server) & [Darkice](https://github.com/rafael2k/darkice)
- python dependencies

### Install LADSPA/Jack plugins

```bash
$ sudo aptitude install invada-studio-plugins-ladspa
$ git clone https://repo.or.cz/ng-jackspa.git
$ sudo aptitude install libglib2.0-dev libncurses5-dev ladspa-sdk ladspa-sdk-dev
$ cd ng-jackspa
# trying to avoid building the GTK version...!
$ make njackspa jackspa-cli
$ ./njackspa /usr/lib/ladspa/inv_input.so 3301
```

### Python dependencies

To use this on Ubuntu 18, you'll need to install jackclient-python's dependencies, which currently means the following:

```bash
$ sudo aptitude install python3-pip
$ python3 -m pip install -r requirements.txt --user
```

### Services

Systemd service files are in `./services`, see the [README.md](./services/README.md) there.

## Usage

If all dependencies are configured correctly you can start the Jackd, Icecast and JackTrip services. Edit the relevant service config files if you want to change the default session configurations.

### hard-coded paths

* Ensure that you have some lounge music path at the currently hard-coded path in [lounge_music.py](./lounge_music.py), currently `/home/sam/lounge-music.mp3`.

* Ensure that you have write access to the currently hard-coded path in [stereo_recording.py](./stereo_recording.py), currently `/home/sam/`. Nb. files will have filenames with prefix `darkice-`, e.g. `darkice-01.wav`.

### Modes

* `jacktrip_pypatcher_mode_2.py` should replicate what the built-in autopatcher does when in `-p2` mode
* `jacktrip_pypatcher.py` should do all the patching you ever need!

#### Mono headphone mix

Some clients would prefer to receive a mono headphone mix, as they can then wear their headphones only on one ear & hear the acoustic sound in their room with their other ear. The easiest thing is for these clients to run jacktrip with `-n1`.

Alternatively they can patch `jacktrip/receive_2` to `system/playback_1` on their local jackd server.

## Run tests

Run tests with:
```bash
$ python3 -m pytest
```

## Credits

Written by Tom Ward ( http://www.madwort.co.uk ) as part of a project with Noise Orchestra ( https://noiseorchestra.org/ )
