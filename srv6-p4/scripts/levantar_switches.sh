#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Por favor, corre este script usando sudo: sudo ./levantar_switches.sh"
  exit 1
fi


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
P4_JSON="$PROJECT_ROOT/build/srv6.json"

echo "Cargando archivo P4 desde: $P4_JSON"

# R1 (Ingress)
simple_switch_grpc --device-id 1 --log-console "$P4_JSON" -i 1@r1-eth1 -i 2@r1-eth2 -i 3@r1-eth3 -- --grpc-server-addr 127.0.0.1:50051 > "$SCRIPT_DIR/logs_r1.log" 2>&1 &

# R2 (Transit Ruta A)
simple_switch_grpc --device-id 2 --thrift-port 9092 --log-console "$P4_JSON" -i 1@r2-eth1 -i 2@r2-eth2 -- --grpc-server-addr 127.0.0.1:50052 > "$SCRIPT_DIR/logs_r2.log" 2>&1 &

# R3 (Transit Ruta B)
simple_switch_grpc --device-id 3 --thrift-port 9093 --log-console "$P4_JSON" -i 1@r3-eth1 -i 2@r3-eth2 -- --grpc-server-addr 127.0.0.1:50053 > "$SCRIPT_DIR/logs_r3.log" 2>&1 &

# R4 (Egress)
simple_switch_grpc --device-id 4 --thrift-port 9094 --log-console "$P4_JSON" -i 1@r4-eth1 -i 2@r4-eth2 -i 3@r4-eth3 -- --grpc-server-addr 127.0.0.1:50054 > "$SCRIPT_DIR/logs_r4.log" 2>&1 &

echo "Switches encendidos"