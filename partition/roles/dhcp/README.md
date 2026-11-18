# dhcp

Configures and starts dhcpd.

This role can deploy on switches running Cumulus Linux or SONiC. It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

```yaml
# Default lease time in seconds.
dhcp_default_lease_time: 172800
# Global deny statements rendered into dhcpd.conf (e.g. unknown-clients).
dhcp_global_deny_list: []
# Global options rendered into dhcpd.conf.
dhcp_global_options: []
# Interfaces the DHCP server listens on.
dhcp_listening_interfaces:
- vlan4000
# Maximum lease time in seconds.
dhcp_max_lease_time: 345600
# Name of the DHCP server service.
dhcp_service_name: '{{ ''dhcpd'' if metal_stack_switch_os_is_cumulus | default(false) else ''isc-dhcp-server'' }}'
# Static host declarations. Each entry supports name, mac and ip.
dhcp_static_hosts: null
# DHCP subnets to serve. Each entry supports comment, network, netmask, range (begin, end) and options.
dhcp_subnets: []
# Whether to enable use-host-decl-names in dhcpd.conf.
dhcp_use_host_decl_names: false
```
