# Automated Firewall Setup with Ansible

This role automates the configuration of management firewalls using Ansible. It is designed to streamline the process of setting up firewalls for consistent deployment before mounting devices in the data center. By utilizing default configurations and flexible variables, this role simplifies the setup across multiple devices.

**Note**: This role is intended to be run on devices reset to factory defaults.

## Supported Devices

| Manufacturer | Model  |
| ------------ | ------ |
| Teltonika    | RUTXR1 |

## Key Features

- **Automated firewall setup** using default configurations
- **VLAN and BGP** configuration support
- **Dynamic port forwarding** setup
- **Pre-configured firewall rules** for LAN, WAN, and global settings
- **Device-specific customization** via `routers.yaml`

## Prerequisites

- The device must be **reset to factory defaults** before running this role.
- An initial login is required to change the root password using credentials defined in the `routers.yaml` file.

## Configuration Details

### Firewall Rules

The firewall is configured with the following settings by default:

1. **Global Settings:**

   - Drop invalid packets: **Enabled**
   - Input: **Drop**
   - Output: **Accept**
   - Forward: **Drop**
   - Offloading: **On**

2. **LAN Configuration:**

   - Input, Output, Forward: **Accept**
   - Masquerading: **On**
   - MSS Clamping: **On**

3. **WAN Configuration:**
   - Input: **Drop**
   - Output: **Accept**
   - Forward: **Drop**
   - Masquerading: **On**
   - MSS Clamping: **On**

### VLAN Configuration

- **VLAN 1:** Tagged to port 4
- **VLAN 2:** Tagged to port 5 (WAN)
- Other VLANs can be configured dynamically.

### BGP Configuration

- The BGP peer is **hardcoded** as `mgmtsrv`.
- The IP address and AS number can be configured dynamically.

## Interfaces

Both LAN and WAN interfaces share the following mandatory fields:

| Field                                                     | Description    |
| --------------------------------------------------------- | -------------- |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.name`         | Interface name |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.ipaddr`       | IP address     |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.netmask`      | Subnet mask    |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.device`       | Router port    |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.dhcp_options` | (LAN Only)     |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.metric`       | (WAN Only)     |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.gateway`      | (WAN Only)     |
| `mgmt_firewall_interfaces.mgmt_firewall_lan.dns` (List)   | (WAN Only)     |

### Default WAN Interface

To enable configuration of the default WAN interface, set `mgmt_firewall_default_wan_enabled` to `true`.

| Field                                                        | Description     |
| ------------------------------------------------------------ | --------------- |
| `mgmt_firewall_interfaces.mgmt_firewall_wan.default.name`    | Interface name  |
| `mgmt_firewall_interfaces.mgmt_firewall_wan.default.ipaddr`  | IP address      |
| `mgmt_firewall_interfaces.mgmt_firewall_wan.default.netmask` | Subnet mask     |
| `mgmt_firewall_interfaces.mgmt_firewall_wan.default.device`  | Router port     |
| `mgmt_firewall_interfaces.mgmt_firewall_wan.default.gateway` | Default gateway |

## Port Forwarding Configuration

The following fields define port forwarding rules:

| Field                                       | Description                    |
| ------------------------------------------- | ------------------------------ |
| `mgmt_firewall_port_forwards.name`          | Rule name                      |
| `mgmt_firewall_port_forwards.src_dport`     | External port                  |
| `mgmt_firewall_port_forwards.dest_ip`       | Internal IP address            |
| `mgmt_firewall_port_forwards.dest_port`     | Internal port                  |
| `mgmt_firewall_port_forwards.src`           | Source zone                    |
| `mgmt_firewall_port_forwards.priority`      | Rule priority (start with 1)   |
| `mgmt_firewall_port_forwards.dest`          | Destination zone               |
| `mgmt_firewall_port_forwards.reflection`    | NAT Loopback (0 = off, 1 = on) |
| `mgmt_firewall_port_forwards.src_ip` (List) | Source IP addresses            |
| `mgmt_firewall_port_forwards.proto` (List)  | Protocols (e.g., TCP, UDP)     |
| `mgmt_firewall_port_forwards.src_dip`       | External IP address            |

## Variables

The following variables can be customized for each firewall:

| Variable                              | Mandatory | Description                                    |
| ------------------------------------- | --------- | ---------------------------------------------- |
| `mgmt_firewall_location_name`         | yes       | Location of the firewall                       |
| `mgmt_firewall_device_name`           | yes       | Device name                                    |
| `mgmt_firewall_public_key`            | yes       | Public key for the firewall                    |
| `mgmt_firewall_default_wan_enabled`   |           | Default: false                                 |
| `mgmt_firewall_wireless_disabled`     |           | Default: true                                  |
| `mgmt_firewall_static_routes_enabled` |           | Set up static routes, by specifying a gateway. |
