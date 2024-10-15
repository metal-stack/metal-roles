# Automatic Setup of Firewalls

This role is meant to setup the management firewalls in an automated fashion through Ansible. Typically, this is executed through a local notebook before mounting the device into the rack of the data center.

The basic setup of the config is always the same so this can be used for every firewall.

**The role is meant to be run on devices that were reset to factory defaults.**

## List of Supported Devices

| Manufacturer | Model        |
| ------------ | ------------ |
| Teltonika    | <model name> |


## Known limitations:

1. Editing bridge interface to off doesnt work off lan.
2. Firewall zones arent working in LAN and WAN interfaces need to adjust manually.
3. There needs to be an inital login to change the root password to the one given in the routers.yaml

## Variables

| Name                        | Mandatory | Description |
| --------------------------- | --------- | ----------- |
| mgmt_firewall_location_name | yes       |             |
| mgmt_firewall_device_name   | yes       |             |
