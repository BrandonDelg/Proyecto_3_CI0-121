#!/bin/bash

mkdir -p build

p4c-bm2-ss \
  --p4v 16 \
  --p4runtime-files build/srv6.p4info.txtpb \
  -o build/srv6.json \
  p4src/main.p4