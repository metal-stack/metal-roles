# prometheus

Deploys prometheus in a systemd-managed Docker container.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../../defaults/README.md).

```yaml
# Basic auth password for the alertmanager.
prometheus_alertmanager_basic_auth_password: null
# Basic auth username for the alertmanager.
prometheus_alertmanager_basic_auth_username: alertmanager
# The alertmanager target (host:port) to send alerts to.
prometheus_alertmanager_target: null
# Scrape targets for the alloy job.
prometheus_alloy_targets: []
# The DNS server probed through the blackbox-exporter.
prometheus_blackbox_exporter_dns: 1.1.1.1
# Groups of icmp probe targets for the blackbox-exporter.
prometheus_blackbox_exporter_icmp_groups: []
# The metal-api URL probed through the blackbox-exporter.
prometheus_blackbox_exporter_metal_api_probe_url: '{{ metal_partition_metal_api_protocol }}://{{ metal_partition_metal_api_addr }}:{{ metal_partition_metal_api_port }}{{ metal_partition_metal_api_basepath }}v1/version'
# Scrape targets for the blackbox-exporter job.
prometheus_blackbox_exporter_targets: []
# Host directory for the prometheus configuration.
prometheus_config_host_dir: /etc/prometheus
# Host directory for the prometheus data.
prometheus_data_host_dir: /var/lib//prometheus
# Docker log driver for the prometheus container.
prometheus_docker_log_driver: json-file
# The global rule evaluation interval.
prometheus_evaluation_interval: 30s
# Scrape targets for the frr-exporter job.
prometheus_frr_exporter_targets: []
# Scrape targets for the gnmic job.
prometheus_gnmic_targets: []
# Whether the haproxy metrics job is scraped.
prometheus_haproxy_enabled: true
# Content of an /etc/hosts file mounted into the prometheus container for static name resolution.
prometheus_hosts_content: null
# Image name of prometheus. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
prometheus_image_name: null
# Image tag of prometheus. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
prometheus_image_tag: null
# CIDRs from which dynamically discovered ipmi targets are allowed.
prometheus_ipmi_exporter_allowed_cidrs: '{{ metal_bmc_allowed_cidrs | default([], '''') }}'
# Static scrape targets for the ipmi job. When empty, targets are generated dynamically from the DHCP leases via a systemd timer.
prometheus_ipmi_exporter_targets: []
# The scrape interval for the ipmi-exporter job.
prometheus_ipmi_scrape_interval: 10m
# The scrape timeout for the ipmi-exporter job.
prometheus_ipmi_scrape_timeout: 120s
# Scrape targets for the lightbox-exporter job.
prometheus_lightbox_exporter_targets: []
# Scrape targets for the lightos smart job.
prometheus_lightos_smart_targets: []
# Scrape targets for the metal-core job.
prometheus_metal_core_targets: []
# Scrape targets for the node-exporter job.
prometheus_node_exporter_targets: []
# Targets for the blackbox-exporter icmp probes.
prometheus_ping_targets: []
# Port prometheus listens on.
prometheus_port: 9090
# Scrape targets for the promtail job.
prometheus_promtail_targets: []
# Remote write configurations rendered into the prometheus configuration.
prometheus_remote_write: []
# Basic auth password that can be referenced from prometheus_remote_write entries.
prometheus_remote_write_basic_auth_password: null
# The global scrape interval.
prometheus_scrape_interval: 60s
# The global scrape timeout.
prometheus_scrape_timeout: 15s
# Scrape targets for the sonic-exporter job.
prometheus_sonic_exporter_targets: []
```
