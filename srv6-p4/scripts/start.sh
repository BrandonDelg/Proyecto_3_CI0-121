#!/bin/bash

BASE_DIR=$(pwd)

echo "Cleaning Mininet..."
sudo mn -c

echo "Scheduling BMv2 switches to start in background..."
(sleep 4; sudo ./scripts/levantar_switches.sh) &

echo "Starting Mininet..."
sudo python3 "$BASE_DIR/topology/topo.py"