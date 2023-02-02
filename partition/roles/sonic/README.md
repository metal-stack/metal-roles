# sonic

Deploys a sonic switch.

## Variables

| Name                       | Mandatory | Description                                                                                |
|----------------------------|-----------|--------------------------------------------------------------------------------------------|
| sonic_mgmt_vrf             | Yes       | Boolean flag to enable / disable the management vrf on the switch.                         |
| sonic_ntpservers           | Yes       | The time servers to use on the switch.                                                     |
| sonic_nameservers          | Yes       | The name servers to use on the switch.                                                     |
| sonic_loopback_address     | Yes       | The loopback address use for this router. Is used to identify routers with bgp unnumbered. |
| sonic_asn                  | Yes       | The autonomous system number of the router.                                                |
| sonic_ip_masquerade        |           | Enable ip masquerading on eth0.                                                            |
| sonic_breakouts            |           | The breakout configuration for ports. E.g. `dict('Ethernet0'='4x25G')`                     |
| sonic_ports                |           | Special configuration for ports (mtu, fec, have highest precedence)                        |
| sonic_ports_default_mtu    |           | MTU Default value for ports                                                                |
| sonic_ports_default_fec    |           | FEC Default value for ports                                                                |
| sonic_bgp_ports            |           | Ports for the underlay BGP sessions                                                        |
| sonic_bgp_ports            |           | Ports for the underlay BGP sessions                                                        |
| sonic_frr_render           |           | Render the frr config                                                                      |
| sonic_frr_debug_options    |           | Debugging options for FRR.                                                                 |
| sonic_frr_syslog_level     |           | Loglevel of FRR                                                                            |
| sonic_frr_l2vpn_evpn       |           | Enable l2vpn evpn as address family.                                                       |
| sonic_frr_route_map        |           | Configure a route map                                                                      |
| sonic_frr_route_map.name   |           | Name of the route map                                                                      |
| sonic_frr_route_map.match  |           | The matcher of the route map                                                               |
| sonic_frr_static_routes    |           | Static routes to be injected through FRR.                                                  |
| sonic_vlans                |           | VLANs to configure.                                                                        |
| sonic_vlans.id             |           | The VLAN ID.                                                                               |
| sonic_vlans.ip             |           | The IP of the SVI of this VLAN.                                                            |
| sonic_vlans.dhcp_servers   |           | Dhcp servers to relay to.                                                                  |
| sonic_vlans.untagged_ports |           | Array of untagged ports to bind to this VLAN.                                              |
| sonic_vteps                |           | VTEPs to configure. If defined FRR will automatically advertise all VNIs.                  |
| sonic_vteps.comment        |           | Description for the VTEP.                                                                  |
| sonic_vteps.vlan           |           | The local VLAN interface.                                                                  |
| sonic_vteps.vni            |           | The global VNI within the CLOS topology.                                                   |
| sonic_lldp_hello_timer     |           | interval for the lldp daemon on the switch to send hello to neighbors                      |