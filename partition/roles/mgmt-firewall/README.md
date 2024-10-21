# Automatic Setup of Firewalls

This role is meant to setup the management firewalls in an automated fashion through Ansible. Typically, this is executed through a local notebook before mounting the device into the rack of the data center.

The basic setup of the config is always the same so this can be used for every firewall.

For easier setup, a main.yaml file in the defaults folder contains all default configuration values.

**The role is meant to be run on devices that were reset to factory defaults.**

## List of Supported Devices

| Manufacturer | Model  |
| ------------ | ------ |
| Teltonika    | RUTXR1 |

## Known limitations:

There needs to be an inital login to change the root password to the one given in the routers.yaml

### Firewall

The firewall is configured the following way:

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

### VLAN

Vlan 1 is tagged the port 4
Vlan 2 is tagged the port 5 (WAN)

Other Vlans can be configured dynamically.

### BGP

BGP peer is hardcoded right now to be named mgmtsrv, the IP and AS can be configured dynamically.

## Interfaces

The following fields are shared between both LAN and WAN interfaces. All of these fields are mandatory unless otherwise specified:

### Common interface fields

| Name         | Description        |
| ------------ | ------------------ |
| name         |                    |
| ipaddr       |                    |
| netmask      |                    |
| device       | Port on the router |
| dhcp_options | (LAN ONLY)         |
| metric       | (WAN ONLY)         |
| gateway      | (WAN ONLY)         |
| dns (List)   | (WAN ONLY)         |

### The Default WAN interface

It's also possible to edit the Default interface, for that set mgmt_firewall_default_wan_enabled to true

| Name    | Description        |
| ------- | ------------------ |
| name    |                    |
| ipaddr  |                    |
| netmask |                    |
| device  | Port on the router |
| gateway |                    |

## Port Forwards

| Name          | Description                                  |
| ------------- | -------------------------------------------- |
| name          |                                              |
| src_dport     | External Port                                |
| dest_ip       | Internal Ip Adress                           |
| dest_port     | Internal Port                                |
| src           | Source Zone                                  |
| priority      | Order when rule applies, start with 1        |
| dest          | Target zone                                  |
| reflection    | Enable NAT Loopback (0 means off,1 means on) |
| src_ip (List) | Source Ip Adresses                           |
| proto (List)  | Protocols (TCP,UDP...)                       |
| src_dip       | External Ip Adress                           |

## Variables

| Name                              | Mandatory | Description       |
| --------------------------------- | --------- | ----------------- |
| mgmt_firewall_location_name       | yes       |                   |
| mgmt_firewall_device_name         | yes       |                   |
| mgmt_firewall_public_key          | yes       |                   |
| mgmt_firewall_default_wan_enabled |           | Defaults to false |
| mgmt_firewall_wireless_disabled   |           | Defaults to true  |
