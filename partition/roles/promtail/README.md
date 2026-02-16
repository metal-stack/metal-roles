# promtail

Deploys promtail in a systemd-managed Docker container.

## Variables

| Name                       | Mandatory | Description                                                                                                        |
| -------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| promtail_config_host_dir   |           | The location of the promtail config                                                                                |
| promtail_image_name        | yes       | Image version of the promtail                                                                                      |
| promtail_image_tag         | yes       | Image tag of the promtail                                                                                          |
| promtail_clients           | yes       | A list of clients for promtail, see <https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#clients> |
| promtail_scrape_configs    | yes       | A list containing the scrape configs                                                                               |
| promtail_docker_log_driver |           | Indicates where to write the docker logs to                                                                        |
