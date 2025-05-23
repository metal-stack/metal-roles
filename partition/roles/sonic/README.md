# sonic

> DEPRECATED: This role is deprecated and replaced by the [sonic-config role](/partition/roles/sonic-config/README.md).

Deploys a SONiC switch. It can run on all switches inside the network topology, i.e. spines, exits, leaves. It is supposed to run on Edgecore SONiC switches.

It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

| Name                                                       | Mandatory | Description                                                                                                          |
| ---------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------- |
| sonic_mgmt_vrf                                             | yes       | Boolean flag to enable / disable the management vrf on the switch.                                                   |
| sonic_ntpservers                                           | yes       | The time servers to use on the switch.                                                                               |
| sonic_nameservers                                          | yes       | The name servers to use on the switch.                                                                               |
| sonic_loopback_address                                     | yes       | The loopback address use for this router. Is used to identify routers with bgp unnumbered.                           |
| sonic_asn                                                  | yes       | The autonomous system number of the router.                                                                          |
| sonic_mgmtif_ip                                            |           | The fixed IP address of the management interface in `IP/netmask` format. If not given, defaults to DHCP.             |
| sonic_mgmtif_gateway                                       |           | If using a fixed management IP, the default gateway for the management interface.                                    |
| sonic_ip_masquerade                                        |           | Enable ip masquerading on eth0.                                                                                      |
| sonic_breakouts                                            |           | The breakout configuration for ports, e.g. `dict('Ethernet0'='4x25G')`                                               |
| sonic_config_action                                        |           | Either `load` or `reload`. In the latter case all services will be restarted. If not given, defaults to `load`       |
| sonic_render_config_db_template                            |           | When `true` the `metal.yaml.j2` template will be rendered into `/etc/sonic/config_db.json`                           |
| sonic_ports                                                |           | Configuration for ports (mtu, fec, have highest precedence). These ports will be up by default.                      |
| sonic_ports.name                                           |           | The port name.                                                                                                       |
| sonic_ports.speed                                          |           | Speed of the port.                                                                                                   |
| sonic_ports.mtu                                            |           | MTU of the port.                                                                                                     |
| sonic_ports.fec                                            |           | FEC used for the port.                                                                                               |
| sonic_ports.vrf                                            |           | VRF where the port should bind to.                                                                                   |
| sonic_ports.ips                                            |           | IPs to assign to the interface directly.                                                                             |
| sonic_ports_default_mtu                                    |           | MTU default value for ports                                                                                          |
| sonic_ports_default_fec                                    |           | FEC default value for ports                                                                                          |
| sonic_ports_default_speed                                  |           | Speed default value for ports                                                                                        |
| sonic_bgp_ports                                            |           | Ports for the underlay BGP sessions                                                                                  |
| sonic_frr_render                                           |           | Render the frr config                                                                                                |
| sonic_frr_debug_options                                    |           | Debugging options for FRR.                                                                                           |
| sonic_frr_syslog_level                                     |           | Log level of FRR                                                                                                     |
| sonic_frr_l2vpn_evpn                                       |           | Enable l2vpn evpn as address family.                                                                                 |
| sonic_frr_route_map                                        |           | Configure a route map                                                                                                |
| sonic_frr_route_map.name                                   |           | Name of the route map                                                                                                |
| sonic_frr_route_map.match                                  |           | The matcher of the route map                                                                                         |
| sonic_frr_static_routes                                    |           | Static routes to be injected through FRR.                                                                            |
| sonic_frr_static_routes_mgmt                               |           | Static routes to be injected to the mgmt VRF.                                                                        |
| sonic_vlans                                                |           | VLANs to configure.                                                                                                  |
| sonic_vlans.id                                             |           | The VLAN ID.                                                                                                         |
| sonic_vlans.ip                                             |           | The IP of the SVI of this VLAN.                                                                                      |
| sonic_vlans.dhcp_servers                                   |           | DHCP servers to relay to.                                                                                            |
| sonic_vlans.untagged_ports                                 |           | Array of untagged ports to bind to this VLAN.                                                                        |
| sonic_vlans.tagged_ports                                   |           | Array of tagged ports to bind to this VLAN.                                                                          |
| sonic_vlans.vrf                                            |           | The VRF to bind the VLANs SVI to.                                                                                    |
| sonic_vlans.sag                                            |           | Whether to enable Static Anycast Gateway for this VLAN. Defaults to false in SONIC.                                  |
| sonic_vteps                                                |           | VTEPs to configure. If defined FRR will automatically advertise all VNIs.                                            |
| sonic_vteps.comment                                        |           | Description for the VTEP.                                                                                            |
| sonic_vteps.vlan                                           |           | The local VLAN interface.                                                                                            |
| sonic_vteps.vni                                            |           | The global VNI within the CLOS topology.                                                                             |
| sonic_lldp_hello_timer                                     |           | Interval for the lldp daemon on the switch to send hello to neighbors                                                |
| sonic_interconnects                                        |           | Configure connections to other BGP parties (e.g. Internet or MPLS routers)                                           |
| sonic_interconnects.sonic_interconnects_default_peer_group |           | The default peer-group name where to put connecting parties.                                                         |
| sonic_interconnects.sonic_interconnects_default_bgp_timers |           | Default bgp timers for connecting parties.                                                                           |
| sonic_interconnects.announcements                          |           | BGP announcements to the connecting parties. (e.g. a static network announcement `network w.x.y.z/24`)               |
| sonic_interconnects.bgp_md5_password                       |           | Use a MD5 password for the BGP session with the remote party.                                                        |
| sonic_interconnects.bgp_timers                             |           | Use specific BGP timer values for the BGP session with the remote party.                                             |
| sonic_interconnects.neighbor_ip                            |           | Connect to this BGP neighbors IP.                                                                                    |
| sonic_interconnects.neighbors                              |           | Connect to this BGP neighbors - supports multiple neighbors and also BGP unnumbered by giving `Ethernet0 interface`. |
| sonic_interconnects.unnumbered_interfaces                  |           | Connect with BGP unnumbered on these interfaces - also sets IPv6 options to make unnumbered work right.              |
| sonic_interconnects.keep_private_as                        |           | Do not remove the privates ASes on this interconnect. For use with static machine ports.                             |
| sonic_interconnects.peer_group                             |           | Put the neighbor in this peer group.                                                                                 |
| sonic_interconnects.evpn_peer                              |           | Whether the peer should take part in evpn routing (address-family l2vpn evpn)                                        |
| sonic_interconnects.prefixlists                            |           | BGP prefix lists to configure.                                                                                       |
| sonic_interconnects.remote_as                              |           | The AS of the BGP neighbor.                                                                                          |
| sonic_interconnects.routemap_in                            |           | Apply an incoming routemap for this BGP session.                                                                     |
| sonic_interconnects.routemap_out                           |           | Apply an outgoing routemap for this BGP session.                                                                     |
| sonic_interconnects.vni                                    |           | This BGP session will connect the specified VNI within the CLOS topology with the given peer.                        |
| sonic_interconnects.vrf                                    |           | Use a dedicated BGP session fenced with an VRF for this connection. Also it declares the virtual network as layer-3. |
| sonic_mclag                                                |           | MCLAG (Multi-Chassis LAG / VPC) configuration for a switch connecting a machine with a LAG bond interface            |
| sonic_mclag.system_mac                                     |           | The shared virtual MAC address used for MCLAG connections                                                            |
| sonic_mclag.peer_ip                                        |           | The IP of the remote switch on the MCLAG peer-link. Corresponds to source_ip.                                        |
| sonic_mclag.peer_link                                      |           | The PortChannel interface connecting the switch pair.                                                                |
| sonic_mclag.source_ip                                      |           | The IP of this switch on the MCLAG peer-link. Corresponds to peer_ip.                                                |
| sonic_mclag.keepalive_vlan                                 |           | The VLAN used for keepalive messages between the MCLAG pair over the peer-link.                                      |
| sonic_mclag.member_port_channels                           |           | A list of the PortChannel numbers that take part in the MCLAG domain.                                                |
| sonic_portchannels_default_mtu                             |           | MTU default value for portchannels                                                                                   |
| sonic_portchannels                                         |           | Configuration for portchannels. These will be up by default.                                                         |
| sonic_portchannels.number                                  |           | The portchannel number                                                                                               |
| sonic_portchannels.mtu                                     |           | The MTU of the portchannel. Must match the MTU of the member ports.                                                  |
| sonic_portchannels.fallback                                |           | Whether to fallback to single port when LAG negotiation fails. Defaults to false in Sonic; does not work with MCLAG. |
| sonic_portchannels.members                                 |           | The list of the interfaces taking part in the portchannel.                                                           |
| sonic_sag                                                  |           | Configuration for SAG (Static Anycast Gateway)                                                                       |
| sonic_sag.mac                                              |           | The virtual MAC used for the SAG address                                                                             |
| sonic_ssh_sourceranges                                     |           | The source ranges from which the switch should be reachable over SSH on its prod (non-management) addresses          |
| sonic_extended_cacl.ipv4                                   |           | Iptables ipv4 rules that should be added as extended Control Plane ACLs (Edgecore Sonic specific feature)            |
| sonic_extended_cacl.ipv6                                   |           | Iptables ipv6 rules that should be added as extended Control Plane ACLs (Edgecore Sonic specific feature)            |

## Configuration hints

### Static machine ports

Sometimes it may be necessary to connect machines to the metal partition that are not managed by metal-stack but need to take part in the bgp routing just like the other machines in the partition; for example certain storage machines.

This can be done by deploying an additional leaf pair without a metal-core, and configuring the machine ports statically with the help of the sonic role.
Since it is not immediately obvious what needs to be configured, here is a short instruction.
Most of the work is done with the sonic_interconnects set of variables as this gives us the necessary BGP instance, neighbor definitions and rroutemaps; but other variables are also necessary.

* You need to configure a local VLAN and VRF with sonic_vlans - define id and vrf - and a matching VTEP with sonic_vteps - define vlan and vni to match the vlan you just created.
* You need to define a sonic_interconnect to create the bgp configuration for the static machines. You need:
  * `vrf`
  * `vni`
  * `peer_group`
  * specify `keep_private_as: true`
  * in `announcements` typically `redistribute connected`
  * routemaps and prefixlists
  * last but not least the machine interfaces.
    * For bgp unnumbered use `unnumbered_interfaces`
    * For "numbered" bgp with interface IPs specify the peers by IP in the `neighbors` section
* Last but not least you need to specify the ports' parameters in the `sonic_ports` section.
  * For bgp unnumbered it is sufficient to define basic parameters like port speed and MTU
  * If you need to define the interface IP for bgp numbered, use `ips`. Then you also need to explicitly seth the vrf with the `vrf` statement.

An example for both bgp unnumbered and numbered can be found in the `static_leaf` test data in the tests for this role.
