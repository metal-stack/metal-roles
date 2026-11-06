# blackbox-exporter

Deploys the blackbox-exporter in a systemd-managed Docker container.

## Variables

```yaml
# Docker log driver for the blackbox-exporter container.
monitoring_blackbox_exporter_docker_log_driver: json-file
# Host directory for the blackbox-exporter configuration.
monitoring_blackbox_exporter_etc_host_dir: /blackbox_exporter
# Image name of the blackbox-exporter.
monitoring_blackbox_exporter_image_name: quay.io/prometheus/blackbox-exporter
# Image tag of the blackbox-exporter.
monitoring_blackbox_exporter_image_tag: v0.24.0
# Port the blackbox-exporter listens on.
monitoring_blackbox_exporter_port: 9115
```
