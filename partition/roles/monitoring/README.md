# monitoring

Deploys exporter in systemd-managed Docker containers.

## Variables

| Name                                             | Mandatory | Description                                                 |
| ------------------------------------------------ | --------- | ----------------------------------------------------------- |
| monitoring_blackbox_exporter_etc_host_dir        |           | The host directory for the blackbox exporter                |
| monitoring_blackbox_exporter_image_name          |           | Image name of the blackblox exporter                        |
| monitoring_blackbox_exporter_image_tag           |           | Image tag of the blackbox exporter                          |
| monitoring_blackbox_exporter_port                |           | Port for the blackblox exporter                             |
| monitoring_ipmi_exporter_etc_host_dir            |           | The host directory for the IPMI exporter                    |
| monitoring_ipmi_exporter_image_name              |           | Image name of the IPMI exporter                             |
| monitoring_ipmi_exporter_image_tag               |           | Image tag of the IPMI exporter                              |
| monitoring_ipmi_exporter_port                    |           | Port for the IPMI exporter                                  |
| monitoring_node_exporter_dir                     |           | The host directory for the node exporter                    |
| monitoring_node_exporter_image_name              |           | Image name of the IPMI exporter                             |
| monitoring_node_exporter_image_tag               |           | Image tag of the IPMI exporter                              |
| monitoring_node_exporter_port                    |           | Port for the IPMI exporter                                  |
| prometheus_port                                  |           | Port for prometheus                                         |
| prometheus_config_host_dir                       |           | The host directory for prometheus configurations            |
| prometheus_data_host_dir                         |           | The host directory for prometheus data                      |
| prometheus_alertmanager_target                   |           | Targets for the alertmanager                                |
| prometheus_alertmanager_basic_auth_username      |           | The username for the authentication to the alertmanager     |
| prometheus_alertmanager_basic_auth_password      |           | The password for the authentication to the alertmanager     |
| prometheus_remote_write                          |           | Remote write target for prometheus                          |
| prometheus_frr_exporter_targets                  |           | FRR exporter targets to scrape from                         |
| prometheus_metal_core_targets                    |           | metal-core targets to scrape from                           |
| prometheus_node_exporter_targets                 |           | Node exporter targets to scrape from                        |
| prometheus_promtail_targets                      |           | Promtail targets to scrape from                             |
| prometheus_ping_targets                          |           | Ping targets to scrape from                                 |
| prometheus_sonic_exporter_targets                |           | Sonic exporter targets to scrape from                       |
| prometheus_blackbox_exporter_targets             |           | Blackbox exporter targets to scrape from                    |
| prometheus_lightbox_exporter_targets             |           | Lightbox exporter targets to scrape from                    |
| prometheus_lightos_smart_targets                 |           | Lightos smart targets to scrape from                        |
| prometheus_hosts_content                         |           | Available hosts for prometheus                              |
| prometheus_blackbox_exporter_icmp_groups         |           | ICMP groups for the blackbox exporter                       |
| prometheus_blackbox_exporter_metal_api_probe_url |           | metal-api probe URL for the blackbox exporter               |
| prometheus_remote_write_basic_auth_username      |           | The username for the prometheus remote write authentication |
| prometheus_remote_write_basic_auth_password      |           | The password for the prometheus remote write authentication |
| sonic_exporter_image_name                        |           | Image name of the sonic exporter                            |
| sonic_exporter_image_tag                         |           | Image tag of the sonic exporter                             |
| sonic_exporter_address                           |           | Address for the sonic exporter                              |
| sonic_exporter_port                              |           | Port for the sonic exporter                                 |
