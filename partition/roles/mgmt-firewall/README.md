# Automatic Setup of Firewalls

This role is meant to setup the management firewalls in an automated fashion through Ansible. Typically, this is executed through a local notebook before mounting the device into the rack of the data center.

The basic setup of the config is always the same so this can be used for every firewall.

**The role is meant to be run on devices that were reset to factory defaults.**

## List of Supported Devices

| Manufacturer | Model  |
| ------------ | ------ |
| Teltonika    | RUTXR1 |

## Known limitations:

1. There needs to be an inital login to change the root password to the one given in the routers.yaml

## Default Settings

### Firewall

Drop invalid packets On

1. Default Settings

   - Input: Drop
   - Output: Accept
   - Forward: Drop
   - Offloading: on

2. Lan:

   - input, output, forward: Accept
   - Masquerading: on
   - MSS clamping: on

3. Wan:

   - input: Drop
   - output: Accept
   - forward: Drop
   - Masquerading: on
   - MSS clamping: on

### BGP

BGP peer is hardcoded right now to be named mgmtsrv, the IP and AS can be configured dynamically.

## Variables

| Name                        | Mandatory | Description |
| --------------------------- | --------- | ----------- |
| mgmt_firewall_location_name | yes       |             |
| mgmt_firewall_device_name   | yes       |             |
