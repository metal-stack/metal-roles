# gnmic

Deploys [gnmic](https://gnmic.openconfig.net/) in a systemd-managed Docker container. It subscribes to the SONiC gNMI server and exposes switch telemetry as Prometheus metrics. Replaces the sonic-exporter.

## Variables

| Name                                      | Mandatory | Description                                        |
| ----------------------------------------- | --------- | -------------------------------------------------- |
| monitoring_gnmic_image_name               |           | Image name of gnmic                                |
| monitoring_gnmic_image_tag                |           | Image tag of gnmic                                 |
| monitoring_gnmic_etc_host_dir             |           | Host directory for the gnmic configuration         |
| monitoring_gnmic_docker_log_driver        |           | Indicates where to write the docker logs to        |
| monitoring_gnmic_gnmi_address             |           | Address of the SONiC gNMI server                   |
| monitoring_gnmic_gnmi_port                |           | Port of the SONiC gNMI server                      |
| monitoring_gnmic_gnmi_username            |           | Username for the gNMI server                       |
| monitoring_gnmic_gnmi_password            |           | Password for the gNMI server                       |
| monitoring_gnmic_gnmi_insecure            |           | Use a plaintext gNMI connection                    |
| monitoring_gnmic_gnmi_skip_verify         |           | Skip TLS certificate verification                  |
| monitoring_gnmic_prometheus_port          |           | Port of the Prometheus metrics endpoint            |
| monitoring_gnmic_ports                    |           | Ports to collect counters for, discovered if empty |
| monitoring_gnmic_disabled_subscriptions   |           | Subscriptions to disable                           |
| monitoring_gnmic_sonic_distribution       |           | SONiC distribution (broadcom/edgecore)             |
| monitoring_gnmic_sample_interval_counters |           | Sample interval for port and queue counters        |
| monitoring_gnmic_sample_interval_state    |           | Sample interval for state tables                   |
| monitoring_gnmic_sample_interval_config   |           | Sample interval for config tables                  |
