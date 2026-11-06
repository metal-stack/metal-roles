# systemd-networkd

Deploys network-configuration for systems using systemd-networkd.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

```yaml
# The default MTU configured on the interfaces.
systemd_networkd_mtu: 9000
# The physical NICs to configure.
systemd_networkd_nics: []
# The VLANs to configure.
systemd_networkd_vlans: []
# The VRFs to configure.
systemd_networkd_vrfs: []
# The VXLANs to configure.
systemd_networkd_vxlans: []
```
