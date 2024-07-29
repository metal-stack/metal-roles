# dhcp

Configures and starts dhcpd.

This role can deploy on switches running Cumulus Linux or SONiC. It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

| Name                      | Mandatory | Description                                                                  |
|---------------------------|-----------|------------------------------------------------------------------------------|
| dhcp_subnets              |           | An array of subnets for which dhcp should lease addresses from               |
| dhcp_subnets.comment      |           | The comment for this dhcp subnet                                             |
| dhcp_subnets.network      | yes       | The dhcp network address in which dhcp addresses will be leased              |
| dhcp_subnets.netmask      | yes       | The netmask of the dhcp network                                              |
| dhcp_subnets.range.begin  | yes       | The smallest address within the dhcp network to offer                        |
| dhcp_subnets.range.end    | yes       | The highest address within the dhcp network to offer                         |
| dhcp_subnets.options      |           | The options for a given subnet                                               |
| dhcp_subnets.deny_list    |           | The deny list for a given subnet                                             |
| dhcp_global_options       |           | The global options                                                           |
| dhcp_global_deny_list     |           | The global deny list                                                         |
| dhcp_static_hosts         |           | The hosts that should get static IPs.                                        |
| dhcp_static_hosts.name    |           | The name for this static mapping.                                            |
| dhcp_static_hosts.mac     |           | The mac for this static mapping.                                             |
| dhcp_static_hosts.ip      |           | The ip for this sstatic mapping.                                             |
| dhcp_static_hosts.options |           | The options to pass to the client with DHCP responses.                       |
| dhcp_use_host_decl_names  |           | The name of the host declaration will be send to the client as its hostname. |
