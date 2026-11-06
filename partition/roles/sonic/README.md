# sonic

> DEPRECATED: This role is deprecated and replaced by the [sonic-config role](/partition/roles/sonic-config/README.md).

Deploys a SONiC switch. It can run on all switches inside the network topology, i.e. spines, exits, leaves. It is supposed to run on Edgecore SONiC switches.

It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

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

## Variables

```yaml
# REQUIRED: The ASN (integer) of the switch used for BGP. Only evaluated when sonic_frr_render is true.
sonic_asn: null
# The ports on which BGP unnumbered sessions are configured.
sonic_bgp_ports: []
# Port breakout configuration keyed by port name.
sonic_breakouts: null
# Whether the generated config_db is applied with config load or config reload.
sonic_config_action: load
# The docker_routing_config_mode of the BGP container.
sonic_docker_routing_config_mode: split
# Extended control plane ACLs (ipv4, ipv6 rule lists) rendered into iptables.json.
sonic_extended_cacl: null
# FRR debug options rendered into frr.conf.
sonic_frr_debug_options: []
# Whether to activate the l2vpn evpn address family.
sonic_frr_l2vpn_evpn: false
# Whether the frr_mgmt_framework_config flag is set in the config_db.
sonic_frr_mgmt_framework_config: true
# Whether to render and deploy the FRR configuration.
sonic_frr_render: true
# Route map (name, match) used for redistributing connected routes.
sonic_frr_route_map: null
# Static routes rendered into frr.conf.
sonic_frr_static_routes: []
# Static routes rendered into frr.conf for the management VRF.
sonic_frr_static_routes_mgmt: []
# The FRR syslog level.
sonic_frr_syslog_level: informational
# Interconnect BGP configuration.
sonic_interconnects: {}
# Default BGP timers for interconnects.
sonic_interconnects_default_bgp_timers: 1 3
# Default peer group for interconnects.
sonic_interconnects_default_peer_group: EXTERNAL
# Whether to activate IP masquerading on eth0.
sonic_ip_masquerade: false
# The LLDP hello timer in seconds.
sonic_lldp_hello_timer: 10
# REQUIRED: The loopback (router) IP address of the switch.
sonic_loopback_address: null
# MCLAG configuration.
sonic_mclag: null
# Whether the management interface is placed in the management VRF.
sonic_mgmt_vrf: true
# Gateway of the management interface.
sonic_mgmtif_gateway: null
# Static IP address (CIDR) of the management interface.
sonic_mgmtif_ip: null
# Nameservers written to /etc/resolv.conf.
sonic_nameservers: []
# NTP servers to configure.
sonic_ntpservers: []
# Port channel configuration.
sonic_portchannels: []
# Default MTU for port channels. Required when sonic_portchannels is non-empty.
sonic_portchannels_default_mtu: null
# Physical port configuration. Each entry supports name and optionally speed, mtu and fec.
sonic_ports: []
# Default FEC for ports that do not specify one.
sonic_ports_default_fec: none
# Default MTU for ports that do not specify one. Required when sonic_ports is non-empty.
sonic_ports_default_mtu: null
# Default speed for ports that do not specify one. Required when sonic_ports is non-empty.
sonic_ports_default_speed: null
# Port configuration keyed by port name. Populated from sonic_ports if left empty.
sonic_ports_dict: {}
# Whether to render and save the config_db from the template.
sonic_render_config_db_template: true
# Static anycast gateway configuration (mac).
sonic_sag: null
# Source ranges from which SSH access is allowed.
sonic_ssh_sourceranges: null
# The timezone to configure on the switch.
sonic_timezone: Europe/Berlin
# Whether VLAN members are rendered into the config_db.
sonic_vlan_members: true
# VLAN configuration. Each entry supports id, ip, untagged_ports and dhcp_servers.
sonic_vlans: []
# VTEP configuration for EVPN.
sonic_vteps: []
```
