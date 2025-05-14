# promtail

Deploys promtail in a systemd-managed Docker container.

## Variables

| Name                                        | Mandatory | Description                                              |
| --------------------------------------------| --------- | -------------------------------------------------------- |
| promtail_config_host_dir                    |           | The location of the promtail config                      |
| promtail_image_name                         | yes       | Image version of the promtail                            |
| promtail_image_tag                          | yes       | Image tag of the promtail                                |
| promtail_clients                            | yes       | A list of clients for promtail                           |
| promtail_clients[*].url                     | yes       | Target URL for the client                                |
| promtail_clients[*].timeout                 |           | Timeout for communicating with the client                |
| promtail_clients[*].basic_auth.username     |           | Username for basic auth at the client                    |
| promtail_clients[*].basic_auth.password     |           | Passord for basic auth at the client                     |
| promtail_scrape_configs                     | yes       | A list containing the scrape configs                     |
