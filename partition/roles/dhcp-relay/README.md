# dhcp-relay

Deploys a dhcp-relay on a switch.

## Variables

```yaml
# The interface to relay DHCP requests from.
dhcp_relay_interface: vlan4000
# REQUIRED: The DHCP server (string) or servers (list of strings) to relay requests to.
dhcp_relay_server: null
```
