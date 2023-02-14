#!/bin/bash

for interface in "${@:2}"; do
   config interface vrf unbind $interface
done