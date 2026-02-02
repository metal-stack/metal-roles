# ipmi-exporter

Deploys the ipmi-exporter in a systemd-managed Docker container.

## Variables

| Name                                       | Mandatory | Description                                 |
| ------------------------------------------ | --------- | ------------------------------------------- |
| monitoring_ipmi_exporter_etc_host_dir      |           | The host directory for the IPMI exporter    |
| monitoring_ipmi_exporter_image_name        |           | Image name of the IPMI exporter             |
| monitoring_ipmi_exporter_image_tag         |           | Image tag of the IPMI exporter              |
| monitoring_ipmi_exporter_port              |           | Port for the IPMI exporter                  |
| monitoring_ipmi_exporter_docker_log_driver |           | Indicates where to write the docker logs to |
| monitoring_ipmi_bmc_superuser              | yes       | Username for the BMC superuser              |
| monitoring_ipmi_bmc_superuser_pwd          | yes       | Password for the BMC superuser              |
