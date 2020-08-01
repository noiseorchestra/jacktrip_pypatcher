#!/bin/bash

jack_lsp | grep receive_ | awk '{print "--port", $1}' | xargs  jack_capture -ns
