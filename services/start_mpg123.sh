#!/bin/bash

sudo killall mpg123.bin
mpg123-jack --name lounge-music --loop -1 ~/lounge-music.mp3
