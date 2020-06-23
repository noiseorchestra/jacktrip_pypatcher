#!/bin/bash

NG_JACKSPA_PATH=~tom/ng-jackspa

$NG_JACKSPA_PATH/jackspa-cli -j right-30 -i '0:0:0:0.3:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-50 -i '0:0:0:0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-65 -i '0:0:0:0.65:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-30 -i '0:0:0:-0.3:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-50 -i '0:0:0:-0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-65 -i '0:0:0:-0.65:0:0' /usr/lib/ladspa/inv_input.so 3301 &
