#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

sudo apt update && sudo apt install python3-tk

python3 -m pip install --user ttkbootstrap --break-system-packages

python3 "$SCRIPT_DIR/app.py"