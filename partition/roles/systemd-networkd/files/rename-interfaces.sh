#!/bin/sh

# Look up the systemd-networkd interface indexes of all ethernet interfaces
ethernets=$(networkctl list |grep ether |awk '{ print $1 }')

for interface in $ethernets; do
  networkctl down $interface
done

# Wait for the interfaces to actually be down
while (networkctl list |grep ether |grep -v off); do
  sleep 10
done
# extra sleep for good measure
sleep 10

systemctl restart systemd-udev-trigger.service

sleep 10

for interface in $ethernets; do
  networkctl up $interface
done
