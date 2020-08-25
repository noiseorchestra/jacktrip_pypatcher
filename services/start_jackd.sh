#!/bin/bash

sudo killall jackd
jackd -d dummy -p256
