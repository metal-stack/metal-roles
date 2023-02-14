#!/bin/bash

for interface in "${@:2}"; do
   config vlan member add ${1} $interface || true
done