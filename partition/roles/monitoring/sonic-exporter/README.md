# sonic-exporter

> [!IMPORTANT]
> This role is deprecated and superseded by the `gnmic` role. New deployments should use `metal-roles/partition/roles/monitoring/gnmic` instead. This role is kept for migration purposes only and may be removed in a future release. See the [gnmic role README](../gnmic/README.md#migrating-from-sonic-exporter) for migration instructions.

Deploys the sonic-exporter in a systemd-managed Docker container.

## Variables

```yaml
# Address the sonic-exporter listens on.
monitoring_sonic_exporter_address: 0.0.0.0
# Docker log driver for the sonic-exporter container.
monitoring_sonic_exporter_docker_log_driver: json-file
# Image name of the sonic-exporter.
monitoring_sonic_exporter_image_name: ghcr.io/metal-stack/sonic-exporter
# Image tag of the sonic-exporter.
monitoring_sonic_exporter_image_tag: main
# Port the sonic-exporter listens on.
monitoring_sonic_exporter_port: 9101
```
