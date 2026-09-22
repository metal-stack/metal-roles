# k3s-server

Configures a k3s server of the autonomous control plane: FRR with BGP unnumbered sessions
to the leaves it is attached to, k3s itself as a member of an HA cluster with embedded
etcd, and metallb as the load balancer that hands out and announces service addresses.

The FRR configuration is rendered here and handed to the [frr](../frr) role, which installs
the packages and deploys it. The k3s binary is downloaded from the release named by
`k3s_server_version` and verified against its published sha256 sum; the official install
script is then run with `INSTALL_K3S_SKIP_DOWNLOAD=true`, so it only creates the systemd
unit, the symlinks and the uninstall script. k3s is configured through
`/etc/rancher/k3s/config.yaml`. The role installs no packages, and depends on fact
gathering.

## The kubernetes api address

Every server carries `k3s_server_api_vip_address` as a `/32` on
`k3s_server_api_vip_interface` and announces it, so the leaves reach the api over ECMP.
metallb cannot serve it: the apiserver is a host process, and a Service-backed endpoint
would make api reachability depend on the cluster's own data plane.

The address belongs to the apiserver process, not to the interface. `k3s-api-vip.service`
is `BindsTo=` and `PartOf=` `k3s.service`, so systemd removes it whenever k3s stops, is
restarted or dies, and adds it again only once the local apiserver answers
`k3s_server_api_vip_probe_url`. FRR follows it through `redistribute connected`.

There is deliberately no periodic poll, so an apiserver that runs but is not ready keeps
the address. A server that loses etcd quorum usually loses its bgp session too, which the
leaves see within the bgp timers, while a poll can be wrong -- an expired certificate or a
moved kubeconfig withdraws a healthy server, and does it on all of them at once.

## Losing a server, and rebuilding it

`cluster-init` is a bootstrap term, not a role a node keeps. k3s ignores the datastore
arguments on a node that already carries a datastore -- "If an etcd datastore is found on
disk ... the datastore arguments (`--cluster-init`, `--server`, `--datastore-endpoint`,
etc) are ignored."

The node with an **empty** disk is the exception, and the probe guards it. Every server
asks the api vip for `/readyz` before `config.yaml` is rendered; if it answers,
`k3s_server_cluster_running` is true and

- no server renders `cluster-init`, not even `k3s_server_cluster_init_host`, which once
  rebuilt would otherwise start a **second** cluster on the same api address,
- every server registers against the api vip instead of one specific loopback,
- `k3s_server_cluster_init_host` no longer has to be reachable, only set, so a deployment
  runs while that server is being replaced.

While nothing answers -- the first bootstrap -- the init host initialises and the others
register against its loopback.

## How metallb reaches the fabric

metallb runs in `native` bgp mode and peers with the FRR **on the same node** over a
node-local dummy interface; FRR re-announces the service `/32`s to the leaves. A node
cannot hold two bgp speakers: the FRR-K8s backend runs its own FRR in the speaker pod with
`hostNetwork: true` and would fight the host FRR for port 179, while the host FRR carries
the node loopback and therefore exists before k3s does. Upstream lists the same limitation:
"It is not possible to peer within the same host (while the native implementation allows
it)."

Which address on that host works is a question about FRR:

- **The dummy interface, not `127.0.0.1`.** Over the loopback address FRR cannot derive a
  nexthop interface and answers the OPEN with `NOTIFICATION 5/0` (`nexthop_set failed ...
  intf (Unknown)`, verified on FRR 10.5.1). Two addresses out of `169.254.254.0/30` on a
  dummy give the session a real interface. The addresses are martian only in the sense
  that they are link-local and not routable beyond this node; the dummy still supplies
  the kernel interface and nexthop FRR needs for the BGP session.
- **`bgp listen range`, not `neighbor <address> remote-as`.** Both ends of this session are
  addresses of this node, and FRR refuses a statically configured neighbor whose address is
  local: `% Can not configure the local system as neighbor`, followed by `Specify remote-as
  or peer-group commands first` for every line that depends on it. The failure is quiet in
  the worst way -- `frr.conf` on disk is correct while the running config simply lacks the
  peer, so only `show bgp summary` shows it. A dynamic neighbor carries no such check: FRR
  accepts the inbound session from the local speaker address. Verified end to end on FRR
  10.7.1, and the static form is rejected on 10.5.1 just the same, so this is not a version
  regression to wait out. The peer-group has to be declared **before** the `bgp listen
  range` line or FRR answers `% Configure the peer-group first`. `passive` is gone with the
  static neighbor: over a listen range FRR only ever accepts. `bgp listen limit` caps
  dynamic peers at 100 by default, which one speaker per node will not reach.
- **`bgp allow-martian-nexthop`.** metallb sets the nexthop to the local address of its own
  tcp connection, an address of this very node, which FRR otherwise drops with `DENIED due
  to: martian or self next-hop`. The option sits under `router bgp` and relaxes the check
  for the leaf sessions too; `K3S_IN_PREFIX` keeps those honest.

`k3s_server_metallb_accept_prefixes` is what FRR accepts from metallb: every entry of
`k3s_server_metallb_addresses` with ` ge 32` appended, written out rather than derived so
the inventory shows what FRR does. The same entries, `ge 32` included, go into
`k3s_server_announce_prefixes`, otherwise a handed-out `/32` matches no OUT entry and stops
at this node. The pool itself is never announced as an aggregate. The session `/30` stays
on the node because `route-map LOOPBACK` filters `redistribute connected` by interface --
`lo` and the api vip interface, nothing else; a prefix-list match there would leak it.

The session addresses are node-local and therefore the same on every server, not read per
host. `k3s_server_cluster_hosts` decides which servers get a `BGPPeer` and defaults to the
play; point it at the inventory group when deploying with a `--limit`, otherwise the run
describes fewer servers than the cluster has and the other peers keep what an earlier run
left behind.

The role applies the upstream manifest of `k3s_server_metallb_version`, then one
`IPAddressPool`, one `BGPAdvertisement` and one `BGPPeer` per server once the crds are
established and the controller serves its validating webhook -- both on the first server of
the play rather than on the init host, so losing that host does not take the metallb
configuration with it.

## Prerequisites

The two dummy interfaces belong to the [systemd-networkd](../systemd-networkd) role, which
has to run first:

```yaml
systemd_networkd_dummies:
  - name: metallb
    addresses:
      - 169.254.254.1/30
      - 169.254.254.2/30
  - name: k3s-vip
```

`k3s-vip` deliberately carries no address; the health gate adds and removes it.

## Variables

| Name                               | Mandatory | Description                                                                             |
|------------------------------------|-----------|-----------------------------------------------------------------------------------------|
| k3s_server_asn                     | x         | The ASN of this server. Must differ from the ASNs of the leaves.                        |
| k3s_server_loopback_address        | x         | The loopback address announced to the leaves. Also the k3s node address.                |
| k3s_server_uplink_interfaces       | x         | The interfaces facing the leaves, one BGP session per interface.                        |
| k3s_server_cluster_init_host       | x         | The inventory host that runs `cluster-init`. All others join it.                        |
| k3s_server_token                   | x         | The cluster token. Must be identical on all servers.                                    |
| k3s_server_cluster_hosts           |           | The servers that form the cluster, one BGPPeer each. Defaults to the play.              |
| k3s_server_router_id               |           | The BGP router id, defaults to the loopback address.                                    |
| k3s_server_peer_group              |           | The name of the BGP peer group, must match the peer group of the leaves.                |
| k3s_server_bgp_timers              |           | The BGP timers of the peer group.                                                       |
| k3s_server_accept_prefixes         |           | The prefixes accepted from the leaves.                                                  |
| k3s_server_announce_prefixes       |           | Announced to the leaves: loopback, api vip, and the pool entries with ' ge 32'.         |
| k3s_server_syslog_level            |           | The syslog level of frr.                                                                |
| k3s_server_version                 |           | The k3s version to install.                                                             |
| k3s_server_install_script_url      |           | Where to fetch the k3s install script from.                                             |
| k3s_server_release_url             |           | The base url the binary and its checksum file are fetched from.                         |
| k3s_server_binary_url              |           | The k3s binary to install. Defaults to the amd64 asset of the pinned release.           |
| k3s_server_checksum_url            |           | The sha256 sum file the binary is verified against.                                     |
| k3s_server_install_script_path     |           | Where the install script is stored on the server.                                       |
| k3s_server_config_dir              |           | The directory holding the k3s configuration.                                            |
| k3s_server_api_port                |           | The port the kubernetes api listens on.                                                 |
| k3s_server_api_timeout             |           | How long a joining server waits for the api of the cluster init server.                 |
| k3s_server_cluster_probe_timeout   |           | How long the probe of the api vip may take.                                             |
| k3s_server_cluster_running         |           | Set to true when the api vip answers. Override it to decide by hand.                    |
| k3s_server_registration_address    |           | What a joining server waits for: the api vip once the cluster runs, else the init host. |
| k3s_server_api_vip_address         |           | The api address all servers carry and announce. Unset disables the api vip.             |
| k3s_server_api_vip_interface       |           | The dummy interface the api vip is added to.                                            |
| k3s_server_api_vip_probe_url       |           | The apiserver path the health gate probes.                                              |
| k3s_server_api_vip_probe_timeout   |           | How long a single readiness probe may take.                                             |
| k3s_server_api_vip_ready_timeout   |           | How long the unit waits for the apiserver before it gives up and stays withdrawn.       |
| k3s_server_api_vip_ready_interval  |           | How often it asks while waiting, and how long systemd waits before retrying.            |
| k3s_server_api_vip_script_path     |           | Where the health gate script is stored on the server.                                   |
| k3s_server_metallb_asn             |           | The ASN metallb uses towards the local FRR. Unset disables metallb.                     |
| k3s_server_metallb_addresses       |           | The addresses metallb hands out, as `IPAddressPool.spec.addresses`.                     |
| k3s_server_metallb_accept_prefixes |           | What frr accepts from metallb. Usually the pool entries with ' ge 32'.                  |
| k3s_server_metallb_version         |           | The metallb version to deploy.                                                          |
| k3s_server_metallb_manifest_url    |           | Where the metallb manifest is fetched from.                                             |
| k3s_server_metallb_manifest_path   |           | Where the metallb manifest is stored on the server.                                     |
| k3s_server_metallb_namespace       |           | The namespace metallb is deployed into.                                                 |
| k3s_server_metallb_pool_name       |           | The name of the address pool and its advertisement.                                     |
| k3s_server_metallb_interface       |           | The dummy interface carrying the session between metallb and FRR.                       |
| k3s_server_metallb_local_address   |           | The FRR side of that session, dialed by metallb.                                        |
| k3s_server_metallb_speaker_address |           | The metallb side of that session, its `sourceAddress` and nexthop.                      |
| k3s_server_metallb_timeout         |           | How long to wait for the metallb crds and controller.                                   |
| k3s_server_cluster_cidr            |           | The pod network. Must be identical on all servers.                                      |
| k3s_server_service_cidr            |           | The service network. Must be identical on all servers.                                  |
| k3s_server_flannel_iface           |           | The interface flannel uses as vxlan tunnel endpoint.                                    |
| k3s_server_flannel_mtu             |           | The underlay MTU flannel derives the tunnel MTU from.                                   |
| k3s_server_tls_sans                |           | Additional addresses to put into the api certificate.                                   |
| k3s_server_disable                 |           | The packaged components not to deploy.                                                  |
| k3s_server_config_extra            |           | Additional keys for `config.yaml`.                                                      |