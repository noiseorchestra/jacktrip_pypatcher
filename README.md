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
$ python3 madwort_auto_patcher.py
```

### Modes

* `madwort_auto_patchen_hubserver_mode_2.py` should replicate what the built-in autopatcher does when in `-p2` mode
* `madwort_auto_patcher.py` should patch a number of mono clients to a stereo mix using ladspa plugins to spread them around the stereo field
* `madwort_auto_patcher_wide.py` should patch a number of mono clients to a stereo mix by patching them only to hard left or right
* `madwort_auto_patcher_tomcount.py` is a fun testing script that will patch multiple mpg123 players to a stereo mix

## Credits

Written by Tom Ward ( http://www.madwort.co.uk ) as part of a project with Noise Orchestra ( https://noiseorchestra.org/ )
