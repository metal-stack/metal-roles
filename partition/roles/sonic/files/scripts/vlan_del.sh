#!/bin/bash

for interface in "${@:2}"; do
   config vlan member del ${1} $interface || true
done