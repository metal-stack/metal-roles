# gnmic

Deploys [gnmic](https://gnmic.openconfig.net/) in a systemd-managed Docker container. It subscribes to the SONiC gNMI server and exposes switch telemetry as Prometheus metrics. Replaces the sonic-exporter.

## Redis load

The SONiC gNMI server serves table and key paths through redis keyspace notifications, in `sample` mode as well as `on-change`. Every subscribed key adds a `PSUBSCRIBE` pattern that redis matches against every write in every database, so per-queue subscriptions (`/COUNTERS/<port>/Queues`) cost tens of percent of redis CPU on a busy switch. Field paths (`/COUNTERS/<port>/SAI_PORT_STAT_<counter>`, `/COUNTERS/<oid>/SAI_QUEUE_STAT_<counter>`) are polled at the sample interval with plain `HGET` instead, which is why port and queue counters are subscribed per field. Field paths must stay in `sample` mode, `on-change` polls them every 200 ms.

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
- NTP metrics (`sonic_ntp_sync_status`, `sonic_ntp_offset`, `sonic_ntp_jitter`) are recording rules over node-exporter data in the `partition-prometheus-rules` role, not gnmic metrics.

### Behavioral differences

- Ports, queues, temperature sensors, fans, CRM ACL tables and transceiver tables are discovered from the switch at deploy time. Subscriptions whose tables are absent, e.g. transceivers on a management switch without optics, are left out because the gNMI server rejects the whole subscription when one table is missing. After changes to port breakout configuration, re-run the role to refresh the subscription lists. Changes to these configurations are uncommon in production.
- Queue counters are subscribed by counter OID from `COUNTERS_QUEUE_NAME_MAP`. If syncd assigns new OIDs after a restart, re-run the role.
- Individual subscriptions can be turned off via `monitoring_gnmic_disabled_subscriptions`. The names match the subscription keys in `gnmic.yaml.j2` (e.g. `state-vxlan`, `counters-crm-acl`).

### Cutover

1. Deploy the gnmic role. Both exporters can run in parallel since they listen on different ports.
2. Add the switches to `prometheus_gnmic_targets` and re-run the prometheus role.
3. Compare metrics from both jobs in Prometheus until you are confident in parity.
4. Update alerts and dashboards to `job="gnmic"`.
5. Remove the switches from `prometheus_sonic_exporter_targets` and re-run the prometheus role.
6. Remove the sonic-exporter from each switch. The role does not do this by design.

Below is an example playbook that can be used to roll out gnmic and the bgp-metrics role and remove the sonic-exporter. The removal step may be omitted for validation as the two services don't conflict.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../../defaults/README.md).

```yaml
# CRM ACL tables to subscribe to. Discovered from the switch at deploy time when left empty.
monitoring_gnmic_crm_acl_tables: []
# Subscription names (as defined in gnmic.yaml.j2) to disable.
monitoring_gnmic_disabled_subscriptions: []
# Docker log driver for the gnmic container.
monitoring_gnmic_docker_log_driver: json-file
# Host directory for the gnmic configuration.
monitoring_gnmic_etc_host_dir: /etc/gnmic
# Fans to subscribe to. Discovered from the switch at deploy time when left empty.
monitoring_gnmic_fans: []
# Address of the gNMI server on the switch.
monitoring_gnmic_gnmi_address: 127.0.0.1
# Whether to connect to the gNMI server without TLS.
monitoring_gnmic_gnmi_insecure: false
# Password for the gNMI server.
monitoring_gnmic_gnmi_password: admin
# Port of the gNMI server on the switch.
monitoring_gnmic_gnmi_port: 8080
# Whether to skip TLS certificate verification for the gNMI server.
monitoring_gnmic_gnmi_skip_verify: true
# Username for the gNMI server.
monitoring_gnmic_gnmi_username: admin
# Heartbeat interval for on-change subscriptions.
monitoring_gnmic_heartbeat_interval: 120s
# Image name of gnmic. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
monitoring_gnmic_image_name: null
# Image tag of gnmic. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
monitoring_gnmic_image_tag: null
# Ports to subscribe to. Discovered from the switch at deploy time when left empty.
monitoring_gnmic_ports: []
# Port on which gnmic exposes prometheus metrics.
monitoring_gnmic_prometheus_port: 9102
# Sample interval for config subscriptions.
monitoring_gnmic_sample_interval_config: 60s
# Sample interval for counter subscriptions.
monitoring_gnmic_sample_interval_counters: 30s
# Sample interval for state subscriptions.
monitoring_gnmic_sample_interval_state: 60s
# The SONiC distribution running on the switch.
monitoring_gnmic_sonic_distribution: broadcom
# Temperature sensors to subscribe to. Discovered from the switch at deploy time when left empty.
monitoring_gnmic_temperature_sensors: []
```
