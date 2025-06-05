# blackbox-exporter

Deploys the blackbox-exporter in a systemd-managed Docker container.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

| Name                                           | Mandatory | Description                                  |
| ---------------------------------------------- | --------- | -------------------------------------------- |
| monitoring_blackbox_exporter_etc_host_dir      |           | The host directory for the blackbox exporter |
| monitoring_blackbox_exporter_image_name        |           | Image name of the blackblox exporter         |
| monitoring_blackbox_exporter_image_tag         |           | Image tag of the blackbox exporter           |
| monitoring_blackbox_exporter_port              |           | Port for the blackblox exporter              |
| monitoring_blackbox_exporter_docker_log_driver |           | Indicates where to write the docker logs to  |
