# systemd-networkd

Deploys network-configuration for systems using systemd-networkd.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

| Name                                     | Mandatory | Description                                                                                         |
| ---------------------------------------- | --------- | --------------------------------------------------------------------------------------------------- |
| systemd_networkd_mtu                     |           | The MTU to use for interfaces.                                                                      |
| systemd_networkd_vrfs                    |           | An array of VRFs to be configured.                                                                  |
| systemd_networkd_vrfs.name               |           | The name of the VRF.                                                                                |
| systemd_networkd_vrfs.table              |           | The routing table id of the VRF.                                                                    |
| systemd_networkd_nics                    |           | An array of network interfaces to be configured. Mac or Name is mandatory.                          |
| systemd_networkd_nics.mac                |           | The MAC of the network interface.                                                                   |
| systemd_networkd_nics.mtu                |           | The MTU to use for this interface.                                                                  |
| systemd_networkd_nics.name               |           | The name this interface will be renamed to.                                                         |
| systemd_networkd_nics.dhcp               |           | Configure the interface addresses with DHCP.                                                        |
| systemd_networkd_nics.dhcpv4routemetrics |           | The metric to apply to routes learned through DHCPv4.                                               |
| systemd_networkd_nics.addresses          |           | array of IP addresses for the interfaces in CIDR notation.                                          |
| systemd_networkd_nics.gateways           |           | array of Gateways IPs for the interfaces.                                                           |
| systemd_networkd_nics.vrf                |           | The VRF to bind this interface to.                                                                  |
| systemd_networkd_nics.vxlans             |           | array of VXLANs to terminate on a physical interface.                                               |
| systemd_networkd_vxlans                  |           | VXLANs to terminate on a server.                                                                    |
| systemd_networkd_vxlans.vtep.iface       |           | The VXLAN interface that should serve as VTEP.                                                      |
| systemd_networkd_vxlans.vtep.vni         |           | The network identifier of a VXLAN - should be unique within a BGP/EVPN-CLOS topology.               |
| systemd_networkd_vxlans.vtep.ip          |           | The IP address of the tunnel endpoint (usually the loopback address when used with bgp unnumbered). |
| systemd_networkd_vxlans.vtep.mtu         |           | The MTU for the VXLAN interface.                                                                    |
| systemd_networkd_vxlans.svi.iface        |           | The VLAN interface that should be attached to the VTEP.                                             |
| systemd_networkd_vxlans.svi.vlanid       |           | The local VLAN ID.                                                                                  |
| systemd_networkd_vxlans.svi.vrf          |           | The VRF that should be used as master device for the VLAN interface.                                |
| systemd_networkd_vxlans.svi.address      |           | The IP address that should be configured at the VLAN interface.                                     |
| systemd_networkd_vxlans.svi.mtu          |           | The MTU for the VLAN interface.                                                                     |

## Examples

```yaml
systemd_network_nics:
- name: lo
  addresses:
  - 127.0.0.1/8
  - 10.1.253.61/32
- name: mgmt
  mac: 3c:ec:ef:fe:93:88
  dhcp: true
  vrf: vrfManagement
- name: prod01
  mac: 6c:fe:54:40:59:70
  vxlans:
  - vni104000
- name: prod02
  mac: 6c:fe:54:40:59:71
  vxlans:
  - vni104000

systemd_network_vrfs:
- name: vrfManagement
  table: 1000
```
