# mgmt-server

Configures a server to act as management server for a metal-stack partition.

## Variables

| Name                                  | Mandatory | Description                                                                     |
|---------------------------------------|-----------|---------------------------------------------------------------------------------|
| mgmt_server_asn                       | yes       | the ASN to use for routing.                                                     |
| mgmt_server_dns_over_tls              |           | whether to use DNSoverTLS (default is true).                                    |
| mgmt_server_firewall_facing_interface | yes       | the interface where the firewall is connected at the management server.         |
| mgmt_server_firewall_ip               |           | the remote ip of the firewall for setting up a numbered BGP session.            |
| mgmt_server_frr_match_interfaces      |           | announce the networks attached to the given interfaces over BGP.                |
| mgmt_server_frr_rep                   |           | the FRR repo to use.                                                            |
| mgmt_server_frr_version               |           | the FRR version to use.                                                         |
| mgmt_server_nameservers               |           | the nameservers to use (default is dns0.eu).                                    |
| mgmt_server_router_id                 | yes       | the router-id to use for routing.                                               |
| mgmt_server_spine_facing_interface    | yes       | the interface where the management spine is connected at the management server. |