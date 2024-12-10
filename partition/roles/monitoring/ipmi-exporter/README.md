# ipmi-exporter

Deploys the ipmi-exporter in a systemd-managed Docker container.

## Variables

| Name                                  | Mandatory | Description                              |
| ------------------------------------- | --------- | ---------------------------------------- |
| monitoring_ipmi_exporter_etc_host_dir |           | The host directory for the IPMI exporter |
| monitoring_ipmi_exporter_image_name   |           | Image name of the IPMI exporter          |
| monitoring_ipmi_exporter_image_tag    |           | Image tag of the IPMI exporter           |
| monitoring_ipmi_exporter_port         |           | Port for the IPMI exporter               |
