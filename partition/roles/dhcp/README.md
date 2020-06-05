# dhcp

Configures and starts dhcpd.

## Variables

| Name             | Mandatory | Description                                                      |
| ---------------- | --------- | ---------------------------------------------------------------- |
| dhcp_net         | yes       | The dhcp network address  in which dhcp addresses will be leased |
| dhcp_netmask     | yes       | The netmask of the dhcp network                                  |
| dhcp_range_min   | yes       | The smallest address within the dhcp network to offer            |
| dhcp_range_max   | yes       | The highest address within the dhcp network to offer             |
| dhcp_server_ip   | yes       |                                                                  |
| dhcp_dns_servers |           | Defines DNS servers for the machines that use this dhcp server   |
