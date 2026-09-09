# k3s-server

Configures a k3s server of the autonomous control plane: FRR with BGP unnumbered sessions
to the leaves it is attached to, and k3s itself as a member of an HA cluster with embedded
etcd.

The FRR configuration is rendered here and handed to the [frr](../frr) role, which installs
the packages and deploys it. The k3s binary is downloaded from the release named by
`k3s_server_version` and verified against its published sha256 sum; the official install
script is then run with `INSTALL_K3S_SKIP_DOWNLOAD=true`, so it only creates the systemd
unit, the symlinks and the uninstall script. k3s is configured through
`/etc/rancher/k3s/config.yaml`. The role installs no packages, and depends on fact
gathering.

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
| k3s_server_release_url          |           | The base url the binary and its checksum file are fetched from.                 |
| k3s_server_binary_url           |           | The k3s binary to install. Defaults to the amd64 asset of the pinned release.   |
| k3s_server_checksum_url         |           | The sha256 sum file the binary is verified against.                             |
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
