# Madwort Auto Patcher

Use [JackClient Python API](https://github.com/spatialaudio/jackclient-python/) to do some autopatching for our [JackTrip](https://github.com/jacktrip/jacktrip) server

## Install

To use this on Ubuntu 18, you'll need to install jackclient-python's dependencies, which currently means the following:

```bash
$ sudo aptitude install python3-pip
$ python3 -m pip install setuptools --user
$ python3 -m pip install cffi --user
$ python3 -m pip install JACK-Client --user
```

## Usage

The hubserver will do its own autopatching, which will fight against you a little bit, disable this with e.g. [this patch to disable the built-in autopatcher](https://github.com/jacktrip/jacktrip/pull/70). Otherwise just run the appropriate script, e.g.

```bash
$ python3 jacktrip_pypatcher.py
```

### Modes

* `jacktrip_pypatcher_mode_2.py` should replicate what the built-in autopatcher does when in `-p2` mode
* `jacktrip_pypatcher.py` should do all the patching you ever need!

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

## Credits

Written by Tom Ward ( http://www.madwort.co.uk ) as part of a project with Noise Orchestra ( https://noiseorchestra.org/ )
