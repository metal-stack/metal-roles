# frr

Configures and starts frr.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

```yaml
# REQUIRED: The complete frr.conf content to deploy.
frr_conf: null
# The FRR repository to install from.
frr_repo: frr-8
# The FRR version to install.
frr_version: 8.4
```
