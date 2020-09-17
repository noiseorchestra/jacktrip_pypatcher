#!/bin/bash

NG_JACKSPA_PATH=~sam/ng-jackspa

$NG_JACKSPA_PATH/jackspa-cli -j centre -i '0:0:0:0:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-15 -i '0:0:0:-0.15:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-30 -i '0:0:0:-0.3:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-45 -i '0:0:0:-0.45:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-60 -i '0:0:0:-0.6:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-75 -i '0:0:0:-0.75:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-15 -i '0:0:0:0.15:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-30 -i '0:0:0:0.3:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-45 -i '0:0:0:0.45:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-60 -i '0:0:0:0.6:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-75 -i '0:0:0:0.75:0:0' /usr/lib/ladspa/inv_input.so 3301 &
