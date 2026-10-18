# sflow-collector

Deploys goflow2 and Vector in systemd-managed Docker containers to collect sFlow samples, enrich them, and send them to Loki.
goflow2 receives sFlow datagrams over UDP on port `6343` by default; it does not use gNMI.
It writes JSON records to a tmpfs spool, which Vector reads and enriches with application protocol names and, depending on the profile, interface, VRF, VNI, ASN, and geographic information.

## Requirements

The collector host needs Docker, systemd, logrotate, and the `ansible.posix` collection for the tmpfs mount.
The role depends on `ansible-common` and the common and partition defaults roles.
Set `metal_partition_id` through the [partition defaults](../defaults/defaults/main.yaml) and provide a reachable Loki endpoint that accepts structured metadata.
Configure the switch to export sFlow to the collector using [`sonic_config_sflow`](../sonic-config/README.md).

The `fabric` and `combined` profiles run the interface mapping exporter on the SONiC switch itself.
It requires Python 3 with the `redis` module, access to the local SONiC Redis CONFIG_DB on `127.0.0.1:6379` (database `4`), Linux interface indices under `/sys/class/net`, and the `ip` command.
Every 60 seconds it publishes mappings to Vector over local HTTP; mappings expire after 180 seconds without a refresh.
The mappings use the sampler address and input interface index to identify a flow's interface, VRF, and VNI.
Collecting samples from other switches does not provide their local interface mappings.

Both Broadcom and Edgecore SONiC deployments must provide working sFlow export and, for fabric enrichment, these local interfaces.
The UDP collector has no gNMI dependency, but that alone does not establish compatibility with every SONiC release; validation on both switch variants is still required.

## Profiles

| Profile | Enrichment |
| --- | --- |
| `fabric` | Application protocol and local interface, VRF, and VNI mappings; no GeoIP or ASN database downloads |
| `edge` | Application protocol, source ASN, and sampled source geolocation; no local SONiC interface mapping exporter |
| `combined` | Both fabric and edge enrichment (default) |

All profiles send flow records to Loki with the `app=goflow2` label.
The edge profiles also send geographic records with `app=goflow2-geo`, using the additional sampling rate below.
The edge profiles download DB-IP Lite city and ASN databases on first deployment and refresh them using `sflow-mmdb-refresh.timer`.
The refresh script tries the current month and then the previous month, and restarts Vector after replacing a database.

## Variables

Defaults are defined in [defaults/main.yaml](defaults/main.yaml).

| Name | Mandatory | Description |
| --- | --- | --- |
| sflow_collector_profile | | `fabric`, `edge`, or `combined`; default `combined` |
| sflow_collector_port | | UDP port receiving sFlow datagrams; default `6343` |
| sflow_collector_metrics_port | | goflow2 HTTP metrics port; default `9099` |
| sflow_collector_internal_port | | Vector's HTTP port on `127.0.0.1` for interface mapping updates in fabric profiles; default `9001` |
| sflow_collector_image_name | | goflow2 container image; default `netsampler/goflow2` |
| sflow_collector_image_tag | | goflow2 image tag; default `latest` |
| sflow_collector_vector_image_name | | Vector container image; default `timberio/vector` |
| sflow_collector_vector_image_tag | | Vector image tag; default `0.55.0-distroless-libc` |
| sflow_collector_vector_geo_sample_rate | | Additional sampling for geographic records, one in N flow events; default `10` |
| sflow_collector_config_host_dir | | Host directory for Vector and logrotate configuration; default `/etc/sflow-collector` |
| sflow_collector_data_host_dir | | Host directory for spool, enrichment databases, and Vector state; default `/var/lib/sflow-collector`; see the refresh script limitation below |
| sflow_collector_loki_endpoint | yes | Loki base URL, for example `https://loki.example.com` |
| sflow_collector_loki_basic_auth_user | | Optional Loki basic authentication username; unset by default |
| sflow_collector_loki_basic_auth_password | | Loki basic authentication password when a username is set; unset by default |
| sflow_collector_loki_tls_verify | | Verify the Loki HTTPS certificate; default `true` |
| sflow_collector_geoip_download_image | | Declared default `alpine:3`; currently unused by the refresh script, which hardcodes that image |
| sflow_collector_docker_log_driver | | Docker log driver for goflow2 and Vector; default `json-file` |
| sflow_collector_spool_tmpfs_size | | Size of the in-memory goflow2 spool; default `256m` |
| sflow_collector_logrotate_size | | Spool file size that triggers rotation when checked; default `32M` |
| sflow_collector_logrotate_keep | | Number of rotated spool files to retain; default `1` |
| sflow_collector_logrotate_interval | | systemd timer interval for checking spool rotation; default `2min` |
| sflow_collector_vector_buffer_max_events | | Maximum events buffered in memory per Loki sink; default `100000`; new events are dropped when full |

The DB-IP refresh script currently fixes its data directory to `/var/lib/sflow-collector` and its download image to `alpine:3`.
Keep the default data directory for `edge` and `combined` deployments.

## Example

On a SONiC switch configured to send its sFlow samples to the local collector:

```yaml
sflow_collector_profile: combined
sflow_collector_loki_endpoint: https://loki.example.com
sflow_collector_loki_basic_auth_user: sflow
sflow_collector_loki_basic_auth_password: "{{ vault_sflow_loki_password }}"
```

To scrape goflow2 metrics, configure the [Prometheus role](../monitoring/prometheus/README.md) with the collector's reachable address:

```yaml
prometheus_goflow2_targets:
  - "192.0.2.10:9099"
```

The [partition Prometheus rules](../../../common/roles/partition-prometheus-rules/README.md) include `partition_prometheus_rules_goflow2` for collector alerts.
Inspect `goflow2.service`, `vector.service`, and, for fabric profiles, `vrf-port-export.service` when troubleshooting ingestion.
