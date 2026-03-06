#!/bin/bash
source "$(dirname "$0")/common.sh"

cd "$BORNE_ROOT/projet/CakeCraft/src"
"$BORNE_ROOT/tools/python_wrapper.sh" main.py
