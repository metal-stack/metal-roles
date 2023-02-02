# systemd-networkd

Deploys network-configuration for systems using systemd-networkd.

## Variables

| Name                                | Mandatory | Description                                                                                         |
|-------------------------------------|-----------|-----------------------------------------------------------------------------------------------------|
| systemd_networkd_mtu                | no        | The MTU to use for interfaces.                                                                      |
| systemd_networkd_vrfs               | no        | An array of VRFs to be configured.                                                                  |
| systemd_networkd_vrfs.name          | no        | The name of the VRF.                                                                                |
| systemd_networkd_vrfs.table         | no        | The routing table id of the VRF.                                                                    |
| systemd_networkd_nics               | no        | An array of network interfaces to be configured. Mac or Name is mandatory.                          |
| systemd_networkd_nics.mac           | no        | The MAC of the network interface.                                                                   |
| systemd_networkd_nics.mtu           | no        | The MTU to use for this interface.                                                                  |
| systemd_networkd_nics.name          | no        | The name this interface will be renamed to.                                                         |
| systemd_networkd_nics.dhcp          | no        | Configure the interface addresses with DHCP.                                                        |
| systemd_networkd_nics.addresses     | no        | array of IP addresses for the interfaces in CIDR notation.                                          |
| systemd_networkd_nics.vrf           | no        | The VRF to bind this interface to.                                                                  |
| systemd_networkd_nics.vxlans        | no        | array of VXLANs to terminate on a physical interface.                                               |
| systemd_networkd_vxlans             | no        | VXLANs to terminate on a server.                                                                    |
| systemd_networkd_vxlans.vtep.iface  | no        | The VXLAN interface that should serve as VTEP.                                                      |
| systemd_networkd_vxlans.vtep.vni    | no        | The network identifier of a VXLAN - should be unique within a BGP/EVPN-CLOS topology.               |
| systemd_networkd_vxlans.vtep.ip     | no        | The IP address of the tunnel endpoint (usually the loopback address when used with bgp unnumbered). |
| systemd_networkd_vxlans.svi.iface   | no        | The VLAN interface that should be attached to the VTEP.                                             |
| systemd_networkd_vxlans.svi.vlanid  | no        | The local VLAN ID.                                                                                  |
| systemd_networkd_vxlans.svi.vrf     | no        | The VRF that should be used as master device for the VLAN interface.                                |
| systemd_networkd_vxlans.svi.address | no        | The IP address that should be configured at the VLAN interface.                                     |

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
