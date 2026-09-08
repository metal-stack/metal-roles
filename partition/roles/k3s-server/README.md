# (TODO - AI generated) k3s-server (TODO - AI generated)

Configures a k3s server of the autonomous control plane: FRR with BGP unnumbered sessions
to the leaves it is attached to, and k3s itself as a member of an HA cluster with embedded
etcd.

The FRR configuration is rendered here and handed to the [frr](../frr) role, which installs
the packages and deploys it. k3s is installed with the official install script, pinned to
`k3s_server_version`, and configured through `/etc/rancher/k3s/config.yaml`. The role
installs on Debian and depends on fact gathering.

## Variables

| Name                            | Mandatory | Description                                                                     |
|---------------------------------|-----------|---------------------------------------------------------------------------------|
| k3s_server_asn                  | x         | The ASN of this server. Must differ from the ASNs of the leaves.                |
| k3s_server_loopback_address     | x         | The loopback address announced to the leaves. Also the k3s node address.        |
| k3s_server_uplink_interfaces    | x         | The interfaces facing the leaves, one BGP session per interface.                |
| k3s_server_cluster_init_host    | x         | The inventory host that runs `cluster-init`. All others join it.                |
| k3s_server_token                | x         | The cluster token. Must be identical on all servers.                            |
| k3s_server_router_id            |           | The BGP router id, defaults to the loopback address.                            |
| k3s_server_peer_group           |           | The name of the BGP peer group, must match the peer group of the leaves.        |
| k3s_server_bgp_timers           |           | The BGP timers of the peer group.                                               |
| k3s_server_accept_prefixes      |           | The prefixes accepted from the leaves.                                          |
| k3s_server_announce_prefixes    |           | The prefixes announced to the leaves.                                           |
| k3s_server_syslog_level         |           | The syslog level of frr.                                                        |
| k3s_server_version              |           | The k3s version to install.                                                     |
| k3s_server_install_script_url   |           | Where to fetch the k3s install script from.                                     |
| k3s_server_install_script_path  |           | Where the install script is stored on the server.                               |
| k3s_server_config_dir           |           | The directory holding the k3s configuration.                                    |
| k3s_server_api_port             |           | The port the kubernetes api listens on.                                         |
| k3s_server_api_timeout          |           | How long a joining server waits for the api of the cluster init server.         |
| k3s_server_cluster_cidr         |           | The pod network. Must be identical on all servers.                              |
| k3s_server_service_cidr         |           | The service network. Must be identical on all servers.                          |
| k3s_server_flannel_iface        |           | The interface flannel uses as vxlan tunnel endpoint.                            |
| k3s_server_flannel_mtu          |           | The underlay MTU flannel derives the tunnel MTU from.                           |
| k3s_server_tls_sans             |           | Additional addresses to put into the api certificate.                           |
| k3s_server_disable              |           | The packaged components not to deploy.                                          |
| k3s_server_config_extra         |           | Additional keys for `config.yaml`.                                              |

The loopback address must be inside the prefix the leaves accept, otherwise the
announcement is discarded by their route-map even though the session is established.

## Why the flannel variables exist

On a server whose only address is a `/32` on `lo` and whose uplinks are unnumbered, k3s
cannot be left to pick the flannel interface itself. Without `k3s_server_flannel_iface`,
flannel takes the interface of the default route, finds no IPv4 address on it and fails to
start; the node never becomes `Ready`.

Pointing `k3s_server_flannel_iface` at `lo` gives flannel the right tunnel endpoint
address, because `127.0.0.1` is filtered out for being neither global nor link-local
unicast. It also gives flannel the wrong MTU: k3s writes `{"Type": "vxlan"}` without an
MTU, so flannel falls back to the MTU of that interface, and `flannel.1` would end up at
`65536 - 50`. Setting `k3s_server_flannel_mtu` makes the role render its own flannel
configuration with an explicit MTU and hand it over with `flannel-conf`.

The alternative is to move the node address off `lo` onto a `dummy` interface with the
right MTU and leave `k3s_server_flannel_mtu` unset. That is the more conventional layout,
but it also touches the FRR route-map that matches on `lo`.

## Why traefik and servicelb are disabled

`servicelb` claims service addresses on the node interfaces and expects the clients to be
L2 adjacent. Between `/32` loopbacks reachable only over BGP there is no such adjacency.
`traefik` is left out because ingress is a deployment decision, not a property of the
partition.

## Known limits

- `k3s_server_version` defaults to `v1.36.4+k3s1`, the stable channel of
  `https://update.k3s.io/v1-release/channels` on 2026-09-08.
- The install script is fetched at deploy time and is not pinned itself; only the binary
  version is. Point `k3s_server_install_script_url` at a mirror to change that.
- A change to `config.yaml` restarts k3s. The restart is serialized across the servers with
  `throttle`, but it is not gated on the api coming back, so a rolling restart of an
  unhealthy cluster can still take quorum with it.
- Whether the kernel accepts a vxlan device whose lower device is `lo` has not been
  measured. `ip -d link show flannel.1` on the node is the test.
