# node-exporter

Deploys the node-exporter in a systemd-managed Docker container.

## Variables

```yaml
# Host directory used by the node-exporter.
monitoring_node_exporter_dir: /node_exporter
# Docker log driver for the node-exporter container.
monitoring_node_exporter_docker_log_driver: json-file
# Image name of the node-exporter.
monitoring_node_exporter_image_name: prom/node-exporter
# Image tag of the node-exporter.
monitoring_node_exporter_image_tag: latest
# Port the node-exporter listens on.
monitoring_node_exporter_port: 9100
# The textfile collector directory on the host.
monitoring_node_exporter_textfile_directory: /var/lib/node_exporter/textfile
```
