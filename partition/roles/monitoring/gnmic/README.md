# gnmic

Deploys [gnmic](https://gnmic.openconfig.net/) in a systemd-managed Docker container. It subscribes to the SONiC gNMI server and exposes switch telemetry as Prometheus metrics. Replaces the sonic-exporter.

## Variables

| Name                                      | Mandatory | Description                                         |
| ----------------------------------------- | --------- | --------------------------------------------------- |
| monitoring_gnmic_image_name               |           | Image name of gnmic                                 |
| monitoring_gnmic_image_tag                |           | Image tag of gnmic                                  |
| monitoring_gnmic_etc_host_dir             |           | Host directory for the gnmic configuration          |
| monitoring_gnmic_docker_log_driver        |           | Indicates where to write the docker logs to         |
| monitoring_gnmic_gnmi_address             |           | Address of the SONiC gNMI server                    |
| monitoring_gnmic_gnmi_port                |           | Port of the SONiC gNMI server                       |
| monitoring_gnmic_gnmi_username            |           | Username for the gNMI server                        |
| monitoring_gnmic_gnmi_password            |           | Password for the gNMI server                        |
| monitoring_gnmic_gnmi_insecure            |           | Use a plaintext gNMI connection                     |
| monitoring_gnmic_gnmi_skip_verify         |           | Skip TLS certificate verification                   |
| monitoring_gnmic_prometheus_port          |           | Port of the Prometheus metrics endpoint             |
| monitoring_gnmic_ports                    |           | Ports to collect counters for, discovered if empty  |
| monitoring_gnmic_temperature_sensors      |           | Temperature sensors to collect, discovered if empty |
| monitoring_gnmic_fans                     |           | Fans to collect, discovered if empty                |
| monitoring_gnmic_crm_acl_tables           |           | CRM ACL tables to collect, discovered if empty      |
| monitoring_gnmic_disabled_subscriptions   |           | Subscriptions to disable                            |
| monitoring_gnmic_sonic_distribution       |           | SONiC distribution (broadcom/edgecore)              |
| monitoring_gnmic_sample_interval_counters |           | Sample interval for port and queue counters         |
| monitoring_gnmic_sample_interval_state    |           | Sample interval for state tables                    |
| monitoring_gnmic_sample_interval_config   |           | Sample interval for config tables                   |
| monitoring_gnmic_heartbeat_interval       |           | Heartbeat interval for on-change subscriptions      |

## Migrating from sonic-exporter

gnmic replaces the sonic-exporter. Instead of reading the Redis databases through
host mounts, it subscribes to the SONiC gNMI server and exposes the same metrics
under their familiar `sonic_*` names.

### Prerequisites

- The SONiC gNMI server must be reachable at `monitoring_gnmic_gnmi_address`/`monitoring_gnmic_gnmi_port` with valid credentials. Override the default credentials in production.
- `monitoring_gnmic_sonic_distribution` must match the switch (`broadcom` or `edgecore`). It selects the stream modes the distribution supports.

### Scrape configuration

| What            | sonic-exporter                      | gnmic                      |
| --------------- | ----------------------------------- | -------------------------- |
| Metrics port    | 9101                                | 9102                       |
| Prometheus role | `prometheus_sonic_exporter_targets` | `prometheus_gnmic_targets` |
| Job label       | `sonic-exporter`                    | `gnmic`                    |

The job label change affects every PromQL expression that filters on
`job="sonic-exporter"`, most notably the `SonicSwitchNotScrapable` alert and the
sonic-exporter Grafana dashboard. Queries against the old job return empty
results without erroring.

### Metric compatibility

- Metric names are kept compatible through the `sonic-metrics.star` processor. Existing dashboards and alerts on `sonic_*` metrics keep working once the job label is updated.
- BGP metrics are not part of gnmic. They come from the separate `bgp-metrics` role.
- NTP metrics (`sonic_ntp_sync_status`, `sonic_ntp_offset`) are recording rules over node-exporter data in the `partition-prometheus-rules` role, not gnmic metrics.

### Behavioral differences

- Ports, temperature sensors, fans and CRM ACL tables are discovered from the switch at deploy time. After changes to port breakout configuration, re-run the role to refresh the subscription lists. Changes to these configurations are uncommon in production.
- Individual subscriptions can be turned off via `monitoring_gnmic_disabled_subscriptions`. The names match the subscription keys in `gnmic.yaml.j2` (e.g. `state-vxlan`, `counters-crm-acl`).

### Cutover

1. Deploy the gnmic role. Both exporters can run in parallel since they listen on different ports.
2. Add the switches to `prometheus_gnmic_targets` and re-run the prometheus role.
3. Compare metrics from both jobs in Prometheus until you are confident in parity.
4. Update alerts and dashboards to `job="gnmic"`.
5. Remove the switches from `prometheus_sonic_exporter_targets` and re-run the prometheus role.
6. Remove the sonic-exporter from each switch. The role does not do this by design.

Below is an example playbook that can be used to roll out gnmic and the bgp-metrics role and remove the sonic-exporter. The removal step may be omitted for validation as the two services don't conflict.

```yaml
---
- name: deploy gnmic
  hosts: <SWITCHES>
  gather_facts: false
  become: true
  roles:
    - name: ansible-common
    - name: metal-roles/partition/roles/monitoring/gnmic
    - name: metal-roles/partition/roles/monitoring/node-exporter
    - name: metal-roles/partition/roles/monitoring/bgp-metrics
  tasks:
    - name: Stop and disable sonic-exporter
      ansible.builtin.systemd:
        name: sonic_exporter
        state: stopped
        enabled: false
      register: sonic_exporter_stop
      failed_when:
        - sonic_exporter_stop is failed
        - "'Could not find the requested service' not in (sonic_exporter_stop.msg | default(''))"

- name: update prometheus scrape config
  hosts: <PROMETHEUS-HOST>
  gather_facts: false
  become: true
  roles:
    - name: ansible-common
    - name: metal-roles/partition/roles/monitoring/prometheus
```
