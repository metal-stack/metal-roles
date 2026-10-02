# dhcp-docker

Configures and starts dhcpd in a docker container.

This role is an alternative to the [dhcp](../dhcp) role and takes the same configuration variables. Instead of installing the `isc-dhcp-server` package, it runs dhcpd from a container image as a systemd service, so it also works on switches that do not provide the package in their apt sources. The container uses the host network, docker must be available on the target.

If the `isc-dhcp-server` package was installed before (e.g. by the [dhcp](../dhcp) role), its services are stopped and disabled. The configuration in `/etc/dhcp` and the leases in `/var/lib/dhcp` are reused.

## Variables

| Name                      | Mandatory | Description                                                                         |
|---------------------------|-----------|-------------------------------------------------------------------------------------|
| dhcp_subnets              |           | An array of subnets for which dhcp should lease addresses from                      |
| dhcp_subnets.comment      |           | The comment for this dhcp subnet                                                    |
| dhcp_subnets.network      | yes       | The dhcp network address in which dhcp addresses will be leased                     |
| dhcp_subnets.netmask      | yes       | The netmask of the dhcp network                                                     |
| dhcp_subnets.range.begin  | yes       | The smallest address within the dhcp network to offer                               |
| dhcp_subnets.range.end    | yes       | The highest address within the dhcp network to offer                                |
| dhcp_subnets.options      |           | The options for a given subnet                                                      |
| dhcp_subnets.deny_list    |           | The deny list for a given subnet                                                    |
| dhcp_listening_interfaces |           | The interfaces on which dhcpd serves requests                                       |
| dhcp_default_lease_time   |           | The default lease time in seconds                                                   |
| dhcp_max_lease_time       |           | The maximum lease time in seconds                                                   |
| dhcp_global_options       |           | The global options                                                                  |
| dhcp_global_deny_list     |           | The global deny list                                                                |
| dhcp_static_hosts         |           | The hosts that should get static IPs.                                               |
| dhcp_static_hosts.name    |           | The name for this static mapping.                                                   |
| dhcp_static_hosts.mac     |           | The mac for this static mapping.                                                    |
| dhcp_static_hosts.ip      |           | The ip for this static mapping.                                                     |
| dhcp_static_hosts.options |           | The options to pass to the client with DHCP responses.                              |
| dhcp_use_host_decl_names  |           | The name of the host declaration will be send to the client as its hostname.        |
| dhcp_service_name         |           | The name of the systemd service running the container                               |
| dhcp_legacy_service_names |           | Services of a package installed dhcp server that get stopped and disabled           |
| dhcp_image_name           |           | The container image providing dhcpd                                                 |
| dhcp_image_tag            |           | The tag of the container image                                                      |
| dhcp_docker_log_driver    |           | The log driver of the container                                                     |
| dhcp_config_dir           |           | The host directory for the dhcpd configuration, mounted to `/etc/dhcp`              |
| dhcp_leases_dir           |           | The host directory for the dhcpd leases, mounted to `/var/lib/dhcp`                 |
