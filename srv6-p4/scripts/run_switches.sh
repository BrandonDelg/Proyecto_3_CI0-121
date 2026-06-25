#!/bin/bash

P4="build/srv6.json"

sudo pkill -f simple_switch_grpc

sleep 2

echo "Starting switches..."

simple_switch_grpc \
  --device-id 1 \
  --grpc-server-addr 127.0.0.1:50051 \
  -i 1@r1-eth1 -i 2@r1-eth2 \
  $P4 > r1.log 2>&1 &

simple_switch_grpc \
  --device-id 2 \
  --grpc-server-addr 127.0.0.1:50052 \
  -i 1@r2-eth1 -i 2@r2-eth2 \
  $P4 > r2.log 2>&1 &

simple_switch_grpc \
  --device-id 3 \
  --grpc-server-addr 127.0.0.1:50053 \
  -i 1@r3-eth1 -i 2@r3-eth2 \
  $P4 > r3.log 2>&1 &

simple_switch_grpc \
  --device-id 4 \
  --grpc-server-addr 127.0.0.1:50054 \
  -i 1@r4-eth1 -i 2@r4-eth2 \
  $P4 > r4.log 2>&1 &

echo "All switches started"