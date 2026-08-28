# k3s-server

Configures FRR on a k3s server of the autonomous control plane: BGP unnumbered sessions
to the leaves it is attached to, announcing its loopback and accepting the default route.

Renders the frr configuration and hands it to the [frr](../frr) role, which installs the
packages and deploys the configuration. It depends on fact gathering.

## Variables

| Name                         | Mandatory | Description                                                             |
|------------------------------|-----------|-------------------------------------------------------------------------|
| k3s_server_asn               | x         | The ASN of this server. Must differ from the ASNs of the leaves.        |
| k3s_server_loopback_address  | x         | The loopback address announced to the leaves.                            |
| k3s_server_uplink_interfaces | x         | The interfaces facing the leaves, one BGP session per interface.        |
| k3s_server_router_id         |           | The BGP router id, defaults to the loopback address.                     |
| k3s_server_peer_group        |           | The name of the BGP peer group, must match the peer group of the leaves. |
| k3s_server_bgp_timers        |           | The BGP timers of the peer group.                                        |
| k3s_server_accept_prefixes   |           | The prefixes accepted from the leaves.                                   |
| k3s_server_announce_prefixes |           | The prefixes announced to the leaves.                                    |
| k3s_server_syslog_level      |           | The syslog level of frr.                                                 |

The loopback address must be inside the prefix the leaves accept, otherwise the
announcement is discarded by their route-map even though the session is established.
