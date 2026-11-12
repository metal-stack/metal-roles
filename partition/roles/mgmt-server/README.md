# mgmt-server

Configures a server to act as management server for a metal-stack partition.

## Variables

```yaml
# REQUIRED: The ASN of the management server used for BGP.
mgmt_server_asn: null
# Whether to enable DNS-over-TLS in systemd-resolved.
mgmt_server_dns_over_tls: true
# The interface where the firewall is connected at the management server.
mgmt_server_firewall_facing_interface: null
# The remote IP of the firewall for setting up a numbered BGP session.
mgmt_server_firewall_ip: null
# Announce the networks attached to the given interfaces over BGP.
mgmt_server_frr_match_interfaces:
- lo
# The FRR repository to use.
mgmt_server_frr_repo: frr-8
# Additional static routes rendered into frr.conf, e.g. "10.4.0.0/24 10.130.0.1".
mgmt_server_frr_static_routes: []
# The FRR version to use.
mgmt_server_frr_version: 8.5-0
# The inventory hosts written to /etc/hosts and the metal user's ssh config.
mgmt_server_metal_ssh_groups: '{{ groups.all }}'
# The filename under which the SSH key pair is stored in /home/metal/.ssh.
mgmt_server_metal_ssh_key_filename: id_rsa
# Additional options rendered into the metal user's ssh config.
mgmt_server_metal_ssh_options: []
# REQUIRED: The SSH private key installed for the metal user.
mgmt_server_metal_ssh_privkey: null
# REQUIRED: The SSH public key installed for the metal user.
mgmt_server_metal_ssh_pubkey: null
# The nameservers to use.
mgmt_server_nameservers:
- 193.110.81.0#dns0.eu
- 2a0f:fc80::#dns0.eu
- 185.253.5.0#dns0.eu
- 2a0f:fc81::#dns0.eu
# If set to true, DHCP routes are not flushed even when a BGP session to the firewall is configured.
mgmt_server_preserve_dhcp_route: null
# Whether the management server announces a default route over BGP.
mgmt_server_provide_default_route: false
# The docker registry mirror to configure in the docker daemon.
mgmt_server_registry_mirror: https://mirror.gcr.io
# REQUIRED: The router-id to use for routing.
mgmt_server_router_id: null
# REQUIRED: The interface where the spine is connected at the management server.
mgmt_server_spine_facing_interface: null
```
