# node-exporter

Deploys the node-exporter in a systemd-managed Docker container.

## Variables

| Name                                       | Mandatory | Description                                 |
| ------------------------------------------ | --------- | ------------------------------------------- |
| monitoring_node_exporter_dir               |           | The host directory for the node exporter    |
| monitoring_node_exporter_image_name        |           | Image name of the IPMI exporter             |
| monitoring_node_exporter_image_tag         |           | Image tag of the IPMI exporter              |
| monitoring_node_exporter_port              |           | Port for the IPMI exporter                  |
| monitoring_node_exporter_docker_log_driver |           | Indicates where to write the docker logs to |
