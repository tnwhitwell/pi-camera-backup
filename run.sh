#!/usr/bin/env bash
filebrowser -c filebrowser.json &
python3 -m flask run --host 0.0.0.0
