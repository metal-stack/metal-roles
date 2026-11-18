# ipmi-exporter

Deploys the ipmi-exporter in a systemd-managed Docker container.

## Variables

```yaml
# The IPMI superuser name used for scraping the machine BMCs.
monitoring_ipmi_bmc_superuser: root
# The IPMI superuser password used for scraping the machine BMCs.
monitoring_ipmi_bmc_superuser_pwd: change-me
# The ipmi-exporter collectors to enable.
monitoring_ipmi_exporter_collectors:
- ipmi
- bmc
- chassis
- sel
- dcmi
# Docker log driver for the ipmi-exporter container.
monitoring_ipmi_exporter_docker_log_driver: json-file
# Host directory for the ipmi-exporter configuration.
monitoring_ipmi_exporter_etc_host_dir: /ipmi_exporter/etc/ipmi_exporter
# Image name of the ipmi-exporter.
monitoring_ipmi_exporter_image_name: prometheuscommunity/ipmi-exporter
# Image tag of the ipmi-exporter.
monitoring_ipmi_exporter_image_tag: v1.6.1
# Port the ipmi-exporter listens on.
monitoring_ipmi_exporter_port: 9290
```
