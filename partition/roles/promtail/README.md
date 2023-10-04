# promtail

Deploys promtail in a systemd-managed Docker container.

## Variables

| Name                        | Mandatory | Description                          |
|-----------------------------|-----------|--------------------------------------|
| promtail_listen_address     |           | The listen address for promtail      |
| promtail_config_host_dir    |           | The location of the promtail config  |
| promtail_image_name         | yes       | Image version of the promtail        |
| promtail_image_tag          | yes       | Image tag of the promtail            |
| promtail_loki_push_endpoint | yes       | The URL to the Loki push endpoint    |
| promtail_scrape_configs     | yes       | A list containing the scrape configs |
