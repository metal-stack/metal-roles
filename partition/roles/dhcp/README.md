# dhcp

Configures and starts dhcpd.

This role can deploy on switches running Cumulus Linux or SONiC. It then requires the `switch_facts` module from `ansible-common` to be run beforehand.

## Variables

| Name                     | Mandatory | Description                                                     |
| ------------------------ | --------- | --------------------------------------------------------------- |
| dhcp_subnets             |           | An array of subnets for which dhcp should lease addresses from  |
| dhcp_subnets.comment     |           | The comment for this dhcp subnet                                |
| dhcp_subnets.network     | yes       | The dhcp network address in which dhcp addresses will be leased |
| dhcp_subnets.netmask     | yes       | The netmask of the dhcp network                                 |
| dhcp_subnets.range.begin | yes       | The smallest address within the dhcp network to offer           |
| dhcp_subnets.range.end   | yes       | The highest address within the dhcp network to offer            |
| dhcp_subnets.options     |           | The options for a given subnet.                                 |
| dhcp_global_options      |           | The global options.                                             |
