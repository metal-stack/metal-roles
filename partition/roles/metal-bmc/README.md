# metal-bmc

Deploys the metal-bmc that gathers information about DHCP leases for ipmi access to servers.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/partition/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/partition/roles/defaults).

```yaml
# Additional volumes to mount into the metal-bmc container.
metal_bmc_additional_volume_mounts: []
# CIDRs from which BMCs are allowed to be reported.
metal_bmc_allowed_cidrs:
- 0.0.0.0/0
# REQUIRED: The IPMI superuser name used to access the machine BMCs.
metal_bmc_bmc_superuser: null
# REQUIRED: The IPMI superuser password used to access the machine BMCs.
metal_bmc_bmc_superuser_pwd: null
# REQUIRED: The console CA certificate content.
metal_bmc_console_ca_cert: null
# REQUIRED: The console certificate content.
metal_bmc_console_cert: null
# Host directory where the console certificates are placed.
metal_bmc_console_cert_dir: '{{ metal_bmc_etc_dir }}/certs/console'
# Group of the console certificate files.
metal_bmc_console_cert_group: root
# Owner of the console certificate files.
metal_bmc_console_cert_owner: root
# REQUIRED: The console certificate key content.
metal_bmc_console_key: null
# Port of the console proxy.
metal_bmc_console_port: 3333
# Docker log driver for the metal-bmc container.
metal_bmc_docker_log_driver: json-file
# The docker network to launch the metal-bmc container in.
metal_bmc_docker_network: null
# MAC addresses ignored by metal-bmc.
metal_bmc_ignore_macs: []
# Image name of metal-bmc. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_bmc_image_name: null
# Image tag of metal-bmc. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_bmc_image_tag: null
# Path to the DHCP lease file evaluated by metal-bmc.
metal_bmc_lease_file: /var/lib/dhcp/dhcpd.leases
# Host directory where the nsq certificates are placed.
metal_bmc_nsq_cert_dir: '{{ metal_bmc_etc_dir }}/certs/nsq'
# Log level for nsq communication.
metal_bmc_nsq_log_level: info
# Whether TLS is used for the nsqd connection. When enabled, the nsqd certificate variables must be set.
metal_bmc_nsq_tls_enabled: true
# REQUIRED: Address (host:port) of the nsqd instance to connect to.
metal_bmc_nsqd_addr: null
# The nsqd CA certificate content. Required when metal_bmc_nsq_tls_enabled is true.
metal_bmc_nsqd_ca_cert: null
# The nsqd client certificate content. Required when metal_bmc_nsq_tls_enabled is true.
metal_bmc_nsqd_client_cert: null
# The nsqd client certificate key content. Required when metal_bmc_nsq_tls_enabled is true.
metal_bmc_nsqd_client_cert_key: null
```
