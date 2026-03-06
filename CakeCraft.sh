#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../../common.sh"

cd "$BORNE_ROOT/projet/CakeCraft/src"
"$BORNE_ROOT/tools/python_wrapper.sh" main.py
