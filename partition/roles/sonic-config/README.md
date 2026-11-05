# sonic-config

> [!NOTE]
> This role replaces the deprecated [sonic](/partition/roles/sonic/README.md) role.
> If you are using the sonic role check the [Migration](#migration-from-the-deprecated-sonic-role) section below.

This role creates a `config_db.json` on a SONiC switch, configures the timezone and adds a `resolv.conf`.
Optionally it may render a `frr.conf` for routing or an `iptables.json` for extended CACL.

## Supported SONiC Versions

The only supported SONiC versions are Edgecore SONiC versions 202111.x and 202211.x.
Other versions might work as well but their behavior might slightly differ for some of the configuration parameters.
For example, if you are using `sonic_config_docker_routing_config_mode: split` on a 202111.x version and wish to migrate to version 202311.5, you will need to use `split-unified` instead.
As the 202111.x versions worked best for us so far this role is mostly tested against those versions.

## Problems with DHCP Relay

Some of our deployments require a DHCP relay agent on the switch which relays PXE boot requests between a client and a PXE server.
From version 202111.6 to version 202111.7 some change in the dhcp_relay broke the relay's ability to forward PXE boot OFFER messages from the server back to the client.
This bug has been fixed in version 202111.11.

## Migration from the Deprecated `sonic` Role

Most of the variables have the same name, meaning and structure as the corresponding ones in the sonic role.
So in most cases simply adding `_config` to the variable name is enough, e.g. `sonic_interconnects` becomes `sonic_config_interconnects`.
Variables that were changed, removed or added are explained below.

### `sonic_ntpservers`

Change

```yaml
sonic_ntpservers:
  - 1.2.3.4
  - 5.6.7.8
```

to

```yaml
sonic_config_ntp:
  servers:
    - 1.2.3.4
    - 5.6.7.8

  # Additionally source interface and VRF can be configured. For example:
  src_interface: Loopback0
  vrf: default
```

### `sonic_mgmtif_ip` and `sonic_mgmtif_gateway`

Change

```yaml
sonic_mgmtif_ip: 10.1.2.3
sonic_mgmtif_gateway: 10.1.2.2
```

to

```yaml
sonic_config_mgmt_interface:
  gateway_address: 10.1.2.2
  ip: 10.1.2.3
```

### `sonic_ip_masquerade`

This variable was removed.
See [this mini-lab PR](https://github.com/metal-stack/mini-lab/pull/237).

### `sonic_config_action`

This variable is replaced by the boolean variable `sonic_config_reload_config` which defaults to `false`.
See [below](#variables) for explanation.

### `sonic_ports`, `sonic_ports_default_speed`, `sonic_ports_default_mtu` and `sonic_ports_default_fec`

All these variables are now gathered in the dictionary `sonic_config_ports`.

Change

```yaml
sonic_ports_default_speed: 100000
sonic_ports_default_mtu: 9000
sonic_ports_default_fec: none

sonic_ports:
  - fec: rs
    ips:
      - 10.0.0.1/32
    mtu: 1420
    name: Ethernet0
    speed: 40000
    vrf: Vrf45
```

to

```yaml
sonic_config_ports:
  # New field to configure default value for auto negotiation. For example:
  default_autoneg: on
  default_fec: none
  default_mtu: 9000
  list:
    # New field to configure auto negotiation per port. For example:
    - autoneg: off
      fec: rs
      ips:
        - 10.0.0.1/32
      mtu: 1420
      name: Ethernet0
      speed: 40000
      vrf: Vrf45
```

`sonic_ports_default_speed` was removed.
The default speed for a port is now derived from its breakout configuration and only a valid alternative speed can override it.

### `sonic_frr_debug_options`

This variable was removed.

### `sonic_interconnects_default_peer_group` and `sonic_interconnects_default_bgp_timers`

These two variables were removed.

### `sonic_portchannels` and `sonic_portchannels_default_mtu`

As with `sonic_ports`, these variables are now combined in one dictionary `sonic_config_portchannels`.

Change

```yaml
sonic_portchannels_default_mtu: 9000

sonic_portchannels:
  - fallback: true
    members:
      - Ethernet0
      - Ethernet1
    mtu: 9000
    number: 01
```

to

```yaml
sonic_config_portchannels:
  default_mtu: 9000
  list:
    - fallback: true
      members:
        - Ethernet0
        - Ethernet1
      mtu: 9000
      number: 01
```

### `sonic_vlan_members`

This variable was removed.

### `sonic_vteps`

Change

```yaml
sonic_vteps:
  - comment: Some comment
    vlan: Vlan3999
    vni: 103999
```

to

```yaml
sonic_config_vtep:
  # New field to configure a VTEP interface even when `vxlan_tunnel_maps` is empty.
  enabled: true
  vxlan_tunnel_maps:
    - vlan: Vlan3999
      vni: 103999
```

## Variables

This section shows an overview of all available variables with example values.

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../defaults/README.md).

```yaml
# The ASN of the switch used for BGP. Required when sonic_config_frr_render is true.
sonic_config_asn: null
# The ports on which BGP unnumbered sessions are configured.
sonic_config_bgp_ports: []
# Port breakout configuration keyed by port name.
sonic_config_breakouts: {}
# The docker_routing_config_mode of the BGP container.
sonic_config_docker_routing_config_mode: split
# Extended control plane ACLs (ipv4, ipv6 rule lists) rendered into iptables.json.
sonic_config_extended_cacl: null
# Feature flags rendered into the config_db.
sonic_config_features: {}
# Whether to activate the l2vpn evpn address family.
sonic_config_frr_l2vpn_evpn: false
# Whether the frr_mgmt_framework_config flag is set in the config_db.
sonic_config_frr_mgmt_framework_config: true
# Prefix lists rendered into frr.conf.
sonic_config_frr_prefixlists: null
# Whether to render and deploy the FRR configuration.
sonic_config_frr_render: true
# Route map (name, match) used for redistributing connected routes.
sonic_config_frr_route_map: {}
# Whether the loopback address is set as default BGP source address.
sonic_config_frr_set_source_address_loopback: true
# Static routes rendered into frr.conf.
sonic_config_frr_static_routes: []
# Static routes rendered into frr.conf for the management VRF.
sonic_config_frr_static_routes_mgmt: []
# The FRR syslog level.
sonic_config_frr_syslog_level: informational
# Interconnect BGP configuration.
sonic_config_interconnects: {}
# The LLDP hello timer in seconds.
sonic_config_lldp_hello_timer: 10
# REQUIRED: The loopback (router) IP address of the switch.
sonic_config_loopback_address: null
# MCLAG configuration.
sonic_config_mclag: {}
# Management interface configuration (ip, gateway).
sonic_config_mgmt_interface: {}
# Whether the management interface is placed in the management VRF.
sonic_config_mgmt_vrf: false
# Nameservers written to /etc/resolv.conf.
sonic_config_nameservers: []
# NTP configuration.
sonic_config_ntp: {}
# Port channel configuration.
sonic_config_portchannels: {}
# Physical port configuration.
sonic_config_ports: null
# Whether the generated config_db is applied with config reload.
sonic_config_reload_config: false
# Static anycast gateway configuration (mac).
sonic_config_sag: null
# Source ranges from which SSH access is allowed.
sonic_config_ssh_sourceranges: []
# The timezone to configure on the switch.
sonic_config_timezone: Europe/Berlin
# VLAN subinterface configuration.
sonic_config_vlan_subinterfaces: []
# VLAN configuration.
sonic_config_vlans: []
# VTEP configuration for EVPN.
sonic_config_vtep: {}
```
