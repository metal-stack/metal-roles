# sonic-exporter

Deploys the sonic-exporter in a systemd-managed Docker container.

## Variables

| Name                         | Mandatory | Description                                 |
| ---------------------------- | --------- | ------------------------------------------- |
| sonic_exporter_image_name    |           | Image name of the sonic exporter            |
| sonic_exporter_image_tag     |           | Image tag of the sonic exporter             |
| sonic_exporter_address       |           | Address for the sonic exporter              |
| sonic_exporter_port          |           | Port for the sonic exporter                 |
| prometheus_docker_log_driver |           | Indicates where to write the docker logs to |
