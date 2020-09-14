#!/bin/bash

NG_JACKSPA_PATH=~sam/ng-jackspa

# For 5 clients
$NG_JACKSPA_PATH/jackspa-cli -j left-50 -i '0:0:0:-0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-50 -i '0:0:0:0.5:0:0' /usr/lib/ladspa/inv_input.so 3301 &

# For 6->11 clients
$NG_JACKSPA_PATH/jackspa-cli -j left-20 -i '0:0:0:-0.2:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-40 -i '0:0:0:-0.4:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-60 -i '0:0:0:-0.6:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j left-80 -i '0:0:0:-0.8:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-20 -i '0:0:0:0.2:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-40 -i '0:0:0:0.4:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-60 -i '0:0:0:0.6:0:0' /usr/lib/ladspa/inv_input.so 3301 &
$NG_JACKSPA_PATH/jackspa-cli -j right-80 -i '0:0:0:0.8:0:0' /usr/lib/ladspa/inv_input.so 3301 &
