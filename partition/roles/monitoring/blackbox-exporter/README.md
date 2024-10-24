# blackbox-exporter

Deploys the blackbox-exporter in a systemd-managed Docker container.

## Variables

| Name                                      | Mandatory | Description                                  |
| ----------------------------------------- | --------- | -------------------------------------------- |
| monitoring_blackbox_exporter_etc_host_dir |           | The host directory for the blackbox exporter |
| monitoring_blackbox_exporter_image_name   |           | Image name of the blackblox exporter         |
| monitoring_blackbox_exporter_image_tag    |           | Image tag of the blackbox exporter           |
| monitoring_blackbox_exporter_port         |           | Port for the blackblox exporter              |
