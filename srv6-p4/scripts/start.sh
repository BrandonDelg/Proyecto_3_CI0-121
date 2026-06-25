#!/bin/bash

BASE_DIR=$(pwd)

echo "Cleaning Mininet..."
sudo mn -c

echo "Starting BMv2 switches..."
./scripts/run_switches.sh

sleep 2


echo "Starting Mininet..."
sudo python3 "$BASE_DIR/topology/topo.py"