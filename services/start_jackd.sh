#!/bin/bash

sudo killall jackd
jackd -R -dalsa -r48000 -p256 -n2 -s -S
