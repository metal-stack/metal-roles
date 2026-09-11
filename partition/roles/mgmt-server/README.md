# mgmt-server

Configures a server to act as management server for a metal-stack partition.

## Variables

| Name                                        | Mandatory | Description                                                                          |
| ------------------------------------------- | --------- | ------------------------------------------------------------------------------------ |
| mgmt_server_asn                             | yes       | the ASN to use for routing.                                                          |
| mgmt_server_dns_over_tls                    |           | whether to use DNSoverTLS (default is true).                                         |
| mgmt_server_firewall_facing_interface       | yes       | the interface where the firewall is connected at the management server.              |
| mgmt_server_firewall_ip                     |           | the remote ip of the firewall for setting up a numbered BGP session.                 |
| mgmt_server_frr_match_interfaces            |           | announce the networks attached to the given interfaces over BGP.                     |
| mgmt_server_frr_repo                        |           | the FRR repo to use.                                                                 |
| mgmt_server_frr_static_routes               |           | additional static routes rendered into frr.conf, e.g. `["10.4.0.0/24 10.130.0.1"]`.  |
| mgmt_server_frr_version                     |           | the FRR version to use.                                                              |
| mgmt_server_nameservers                     |           | the nameservers to use (default is dns0.eu).                                         |
| mgmt_server_router_id                       | yes       | the router-id to use for routing.                                                    |
| mgmt_server_spine_facing_interface          | yes       | the interface where the management spine is connected at the management server.      |
| mgmt_server_metal_ssh_key_filename          |           | the filename of the private ssh key                                                  |
| mgmt_server_metal_ssh_groups                |           | the ansible group to include into the ssh config                                     |
| mgmt_server_metal_ssh_options               |           | the options to add globally to the ssh config                                        |
| mgmt_server_metal_ssh_privkey               | yes       | the private SSH key of the `metal` admin user for connecting to the other components |
| mgmt_server_metal_ssh_pubkey                | yes       | the public SSH key of the `metal` admin user for connecting to the other components  |
| mgmt_server_preserve_dhcp_route             | no        | preserve the dhcp (default) route the mgmt server got from the mgmt firewall         |
| mgmt_server_provide_default_route           | no        | provide the default route with bgp (`network 0.0.0.0/0`)                             |
| mgmt_server_vrfs                            | no        | additional BGP instances in VRFs, see [VRFs](#vrfs).                                 |
| mgmt_server_masquerade_interfaces           | no        | the interfaces on which egressing traffic is masqueraded.                            |
| mgmt_server_masquerade_exclude_destinations | no        | what is exempted from masquerading, see [Masquerading](#masquerading).               |

## VRFs

`mgmt_server_vrfs` renders an additional `router bgp <asn> vrf <name>` instance per entry,
each with its own `FABRIC` peer group of unnumbered sessions. Use it to reach a network
that must stay separate from the default VRF.

```yaml
mgmt_server_vrfs:
  - name: vrfACPmgmt
    router_id: 10.0.0.1
    bgp_timers: 1 3
    unnumbered_interfaces:
      - vlan11
    announcements:
      - redistribute connected
    routemap_out:
      name: RM_ACP_OUT
      entries:
        - match ip address prefix-list PL_ACP_OUT
```

| Key                   | Mandatory | Description                                                            |
| --------------------- | --------- | ---------------------------------------------------------------------- |
| name                  | yes       | the name of the VRF, which must already exist on the host.             |
| unnumbered_interfaces | yes       | the interfaces carrying one BGP session each.                          |
| router_id             |           | the BGP router id, defaults to `mgmt_server_router_id`.                |
| bgp_timers            |           | the timers of the peer group, default `1 3`.                           |
| announcements         |           | the lines in the address family, default `redistribute connected`.     |
| routemap_out          |           | a route map applied outbound, given as `name` and a list of `entries`. |

Receiving DHCP and TCP through a VRF needs `net.ipv4.udp_l3mdev_accept` and
`net.ipv4.tcp_l3mdev_accept`, which this role sets.

## Masquerading

`mgmt_server_masquerade_interfaces` appends one `POSTROUTING -o <interface> -j MASQUERADE`
per interface. `mgmt_server_masquerade_exclude_destinations` inserts a `RETURN` above those
rules, so the listed traffic is routed with its original source address. An entry is either
a destination prefix, or a mapping that also restricts the exemption by source.

```yaml
mgmt_server_masquerade_interfaces:
  - vlan4000
mgmt_server_masquerade_exclude_destinations:
  - 10.4.0.0/24
  - destination: 10.5.0.0/24
    source: 10.1.0.0/24
```
