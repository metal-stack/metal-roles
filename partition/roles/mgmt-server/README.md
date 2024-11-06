# mgmt-server

Configures a server to act as management server for a metal-stack partition.

## Variables

| Name                                  | Mandatory | Description                                                                          |
| ------------------------------------- | --------- | ------------------------------------------------------------------------------------ |
| mgmt_server_asn                       | yes       | the ASN to use for routing.                                                          |
| mgmt_server_dns_over_tls              |           | whether to use DNSoverTLS (default is true).                                         |
| mgmt_server_firewall_facing_interface | yes       | the interface where the firewall is connected at the management server.              |
| mgmt_server_firewall_ip               |           | the remote ip of the firewall for setting up a numbered BGP session.                 |
| mgmt_server_frr_match_interfaces      |           | announce the networks attached to the given interfaces over BGP.                     |
| mgmt_server_frr_repo                  |           | the FRR repo to use.                                                                 |
| mgmt_server_frr_version               |           | the FRR version to use.                                                              |
| mgmt_server_nameservers               |           | the nameservers to use (default is dns0.eu).                                         |
| mgmt_server_router_id                 | yes       | the router-id to use for routing.                                                    |
| mgmt_server_spine_facing_interface    | yes       | the interface where the management spine is connected at the management server.      |
| mgmt_server_metal_ssh_groups          |           | the ansible group to include into the ssh config                                     |
| mgmt_server_metal_ssh_options         |           | the options to add globally to the ssh config                                        |
| mgmt_server_metal_ssh_privkey         | yes       | the private SSH key of the `metal` admin user for connecting to the other components |
| mgmt_server_metal_ssh_pubkey          | yes       | the public SSH key of the `metal` admin user for connecting to the other components  |
| mgmt_server_preserve_dhcp_route       | no        | preserve the dhcp (default) route the mgmt server got from the mgmt firewall         |
| mgmt_server_provide_default_route     | no        | provide the default route with bgp (`network 0.0.0.0/0`)                             |
