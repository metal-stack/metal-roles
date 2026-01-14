# sonic-exporter

Deploys the sonic-exporter in a systemd-managed Docker container.

## Variables

| Name                                        | Mandatory | Description                                 |
| ------------------------------------------- | --------- | ------------------------------------------- |
| monitoring_sonic_exporter_image_name        |           | Image name of the sonic exporter            |
| monitoring_sonic_exporter_image_tag         |           | Image tag of the sonic exporter             |
| monitoring_sonic_exporter_address           |           | Address for the sonic exporter              |
| monitoring_sonic_exporter_port              |           | Port for the sonic exporter                 |
| monitoring_sonic_exporter_docker_log_driver |           | Indicates where to write the docker logs to |
