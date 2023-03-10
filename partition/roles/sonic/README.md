# sonic

Deploys a sonic switch.

## Variables

| Name                                                       | Mandatory | Description                                                                                                          |
|------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| sonic_mgmt_vrf                                             | Yes       | Boolean flag to enable / disable the management vrf on the switch.                                                   |
| sonic_ntpservers                                           | Yes       | The time servers to use on the switch.                                                                               |
| sonic_nameservers                                          | Yes       | The name servers to use on the switch.                                                                               |
| sonic_loopback_address                                     | Yes       | The loopback address use for this router. Is used to identify routers with bgp unnumbered.                           |
| sonic_asn                                                  | Yes       | The autonomous system number of the router.                                                                          |
| sonic_mgmtif_ip                                            |           | The fixed IP address of the management interface. If none is given, defaults to dynamic assignment through DHCP.     |
| sonic_mgmtif_gateway                                       |           | If using a fixed management IP, the default gateway for the management interface.                                    |
| sonic_ip_masquerade                                        |           | Enable ip masquerading on eth0.                                                                                      |
| sonic_breakouts                                            |           | The breakout configuration for ports. E.g. `dict('Ethernet0'='4x25G')`                                               |
| sonic_ports                                                |           | Special configuration for ports (mtu, fec, have highest precedence)                                                  |
| sonic_ports.name                                           |           | The port name.                                                                                                       |
| sonic_ports.speed                                          |           | Speed of the port.                                                                                                   |
| sonic_ports.mtu                                            |           | MTU of the port.                                                                                                     |
| sonic_ports.fec                                            |           | FEC used for the port.                                                                                               |
| sonic_ports.vrf                                            |           | VRF where the port should be bound to.                                                                               |
| sonic_ports.ips                                            |           | IPs to assign to the interface directly.                                                                             |
| sonic_ports_default_mtu                                    |           | MTU Default value for ports                                                                                          |
| sonic_ports_default_fec                                    |           | FEC Default value for ports                                                                                          |
| sonic_ports_default_speed                                  |           | Speed Default value for ports                                                                                        |
| sonic_bgp_ports                                            |           | Ports for the underlay BGP sessions                                                                                  |
| sonic_frr_render                                           |           | Render the frr config                                                                                                |
| sonic_frr_debug_options                                    |           | Debugging options for FRR.                                                                                           |
| sonic_frr_syslog_level                                     |           | Loglevel of FRR                                                                                                      |
| sonic_frr_l2vpn_evpn                                       |           | Enable l2vpn evpn as address family.                                                                                 |
| sonic_frr_route_map                                        |           | Configure a route map                                                                                                |
| sonic_frr_route_map.name                                   |           | Name of the route map                                                                                                |
| sonic_frr_route_map.match                                  |           | The matcher of the route map                                                                                         |
| sonic_frr_static_routes                                    |           | Static routes to be injected through FRR.                                                                            |
| sonic_frr_static_routes_mgmt                               |           | Static routes to be injected to the mgmt VRF.                                                                        |
| sonic_vlans                                                |           | VLANs to configure.                                                                                                  |
| sonic_vlans.id                                             |           | The VLAN ID.                                                                                                         |
| sonic_vlans.ip                                             |           | The IP of the SVI of this VLAN.                                                                                      |
| sonic_vlans.dhcp_servers                                   |           | Dhcp servers to relay to.                                                                                            |
| sonic_vlans.untagged_ports                                 |           | Array of untagged ports to bind to this VLAN.                                                                        |
| sonic_vlans.vrf                                            |           | The VRF to bind the VLANs SVI to.                                                                                    |
| sonic_vteps                                                |           | VTEPs to configure. If defined FRR will automatically advertise all VNIs.                                            |
| sonic_vteps.comment                                        |           | Description for the VTEP.                                                                                            |
| sonic_vteps.vlan                                           |           | The local VLAN interface.                                                                                            |
| sonic_vteps.vni                                            |           | The global VNI within the CLOS topology.                                                                             |
| sonic_lldp_hello_timer                                     |           | interval for the lldp daemon on the switch to send hello to neighbors                                                |
| sonic_interconnects                                        |           | Configure connections to other BGP parties (e.g. Internet or MPLS routers)                                           |
| sonic_interconnects.sonic_interconnects_default_peer_group |           | The default peer-group name where to put connecting parties.                                                         |
| sonic_interconnects.sonic_interconnects_default_bgp_timers |           | Default bgp timers for connecting parties.                                                                           |
| sonic_interconnects.announcements                          |           | BGP announcements to the connecting parties. (e.g. a static network announcement `network w.x.y.z/24`)               |
| sonic_interconnects.bgp_md5_password                       |           | Use a MD5 password for the BGP session with the remote party.                                                        |
| sonic_interconnects.bgp_timers                             |           | Use specific BGP timer values for the BGP session with the remote party.                                             |
| sonic_interconnects.neighbor_ip                            |           | Connect to this BGP neighbors IP.                                                                                    |
| sonic_interconnects.neighbors                              |           | Connect to this BGP neighbors - supports multiple neighbors and also BGP unnumbered by giving `Ethernet0 interface`. |
| sonic_interconnects.peer_group                             |           | Put the neighbor in this peer group.                                                                                 |
| sonic_interconnects.prefixlists                            |           | BGP Prefix Lists to configure.                                                                                       |
| sonic_interconnects.remote_as                              |           | The AS of the BGP neighbor.                                                                                          |
| sonic_interconnects.routemap_in                            |           | Apply an incoming routemap for this BGP session.                                                                     |
| sonic_interconnects.routemap_out                           |           | Apply an outgoing routemap for this BGP session.                                                                     |
| sonic_interconnects.vni                                    |           | This BGP session will connect the specified VNI within the CLOS topology with the given peer.                        |
| sonic_interconnects.vrf                                    |           | Use a dedicated BGP session fenced with an VRF for this connection. Also it declares the virtual network as layer-3. |
