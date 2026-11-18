# promtail

> [!IMPORTANT]
> This role is deprecated and superseded by the `alloy` role. New deployments should use `metal-roles/partition/roles/alloy` instead. This role is kept for migration purposes only and may be removed in a future release. See the [alloy role README](../alloy/README.md) for migration instructions.

Deploys promtail in a systemd-managed Docker container.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../defaults/README.md).

```yaml
# Loki client configurations rendered into the promtail configuration. Must not be empty.
promtail_clients: []
# The location of the promtail config on the host.
promtail_config_host_dir: /etc/promtail
# Docker log driver for the promtail container.
promtail_docker_log_driver: json-file
# Image name of promtail. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
promtail_image_name: null
# Image tag of promtail. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
promtail_image_tag: null
# Scrape configs rendered into the promtail configuration. Must not be empty.
promtail_scrape_configs: []
```
