#!/bin/bash

for interface in "${@:2}"; do
   config interface vrf bind $interface ${1}
done