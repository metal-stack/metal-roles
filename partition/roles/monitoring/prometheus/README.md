# prometheus

Deploys prometheus in a systemd-managed Docker container.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure
you define them adequately as well.

| Name                                             | Mandatory | Description                                                                                                                               |
| ------------------------------------------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| prometheus_port                                  |           | Port for prometheus                                                                                                                       |
| prometheus_docker_log_driver                     |           | Indicates where to write the docker logs to                                                                                               |
| prometheus_image_name                            | yes       | Image version of the prometheus                                                                                                           |
| prometheus_image_tag                             | yes       | Image tag of the prometheus                                                                                                               |
| prometheus_config_host_dir                       |           | The host directory for prometheus configurations                                                                                          |
| prometheus_data_host_dir                         |           | The host directory for prometheus data                                                                                                    |
| prometheus_alertmanager_target                   |           | Targets for the alertmanager                                                                                                              |
| prometheus_alertmanager_basic_auth_username      |           | The username for the authentication to the alertmanager                                                                                   |
| prometheus_alertmanager_basic_auth_password      |           | The password for the authentication to the alertmanager                                                                                   |
| prometheus_remote_write                          |           | A list of remote write targets for prometheus, see https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write |
| prometheus_frr_exporter_targets                  |           | FRR exporter targets to scrape from                                                                                                       |
| prometheus_metal_core_targets                    |           | metal-core targets to scrape from                                                                                                         |
| prometheus_node_exporter_targets                 |           | Node exporter targets to scrape from                                                                                                      |
| prometheus_promtail_targets                      |           | Promtail targets to scrape from                                                                                                           |
| prometheus_ping_targets                          |           | Ping targets to scrape from                                                                                                               |
| prometheus_sonic_exporter_targets                |           | Sonic exporter targets to scrape from                                                                                                     |
| prometheus_blackbox_exporter_targets             |           | Blackbox exporter targets to scrape from                                                                                                  |
| prometheus_blackbox_exporter_dns                 |           | Blackbox exporter DNS resolve nameserver                                                                                                  |
| prometheus_lightbox_exporter_targets             |           | Lightbox exporter targets to scrape from                                                                                                  |
| prometheus_lightos_smart_targets                 |           | Lightos smart targets to scrape from                                                                                                      |
| prometheus_ipmi_exporter_targets                 |           | IPMI exporter targets to scrape from                                                                                                      |
| prometheus_hosts_content                         |           | Available hosts for prometheus                                                                                                            |
| prometheus_blackbox_exporter_icmp_groups         |           | ICMP groups for the blackbox exporter                                                                                                     |
| prometheus_blackbox_exporter_metal_api_probe_url |           | metal-api probe URL for the blackbox exporter                                                                                             |
| prometheus_scrape_interval                       |           | The frequency to scrape targets                                                                                                           |
| prometheus_evaluation_interval                   |           | The frequency to evaluate rules                                                                                                           |
| prometheus_scrape_timeout                        |           | Timeout per-scrape                                                                                                                        |
| prometheus_haproxy_enabled                       |           | Enable HAProxy metrics scraping                                                                                                           |
