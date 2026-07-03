# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend, running in [monolithic mode](https://grafana.com/docs/loki/latest/get-started/deployment-modes/#monolithic-mode) on a persistent volume
- **Alloy** — log collector (DaemonSet) via [logging-common](../logging-common/)
- Loki gateway (NGINX) with ingress, optional TLS and basic auth

Alloy is deployed by default. Existing Promtail installations are automatically removed when the role runs.
Alloy configuration, labels, meta-monitoring, and migration guidance are in [logging-common](../logging-common/).

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every
> run. See the [migration guide](../logging-common/README.md#migration-from-promtail).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

### Loki

| Name                                          | Mandatory | Default                                      | Description                                                                                                                                                             |
| --------------------------------------------- | --------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_chart_version                         | yes       |                                              | Helm chart version for loki (release vector)                                                                                                                            |
| logging_chart_repo                            | yes       |                                              | Repository for loki (release vector)                                                                                                                                    |
| logging_namespace                             |           | `monitoring`                                 | Target namespace                                                                                                                                                        |
| logging_loki_size                             |           | `30Gi`                                       | PVC size for all Loki data (chunks, index, WAL, compactor scratch). Size as: `daily_compressed_volume × retention_days × 1.2`.                                          |
| logging_loki_storage_class                    |           | `null` (cluster default)                     | StorageClass for the Loki PVC — must support `ReadWriteOnce`. **Set explicitly** in production to a fast block-storage class (e.g. `premium-rwo`).                      |
| logging_loki_log_level                        |           | `warn`                                       | Loki server log level: `debug`, `info`, `warn`, `error`.                                                                                                                |
| logging_loki_retention_enabled                |           | `true`                                       | Enable automatic log expiry via the compactor. When `false`, logs are kept forever and the deletion API is disabled.                                                    |
| logging_loki_retention_period                 |           | `30d`                                        | Global retention TTL. Minimum `24h`, must be a multiple of `24h`. Use `Nd` or `Nh` format (e.g. `30d`, `48h`). Only active when `logging_loki_retention_enabled: true`. |
| logging_loki_deletion_mode                    |           | `filter-and-delete`                          | `filter-and-delete`: physically removes data from storage (required for GDPR). `filter-only`: hides from queries only. `disabled`: deletion API off.                    |
| logging_loki_retention_stream                 |           | `[]`                                         | Per-stream retention rules evaluated before the global period. See [Retention](#retention) below.                                                                       |
| logging_loki_monitoring_enabled               |           | `false`                                      | Enable ServiceMonitor, PrometheusRule (alerts + recording rules) and Grafana dashboard ConfigMaps. Requires the [monitoring role](../monitoring/) to be deployed first. |
| logging_ingress_enabled                       |           | `false`                                      | If enabled, deploys an Ingress resource for Loki.                                                                                                                       |
| logging_ingress_dns                           |           | `loki.{{ metal_control_plane_ingress_dns }}` | DNS name for the Loki ingress                                                                                                                                           |
| logging_ingress_loki_tls                      |           | `true`                                       | Expose Loki over HTTPS on the ingress                                                                                                                                   |
| logging_ingress_loki_basic_auth_user          |           | `promtail`                                   | Basic auth username for the external Loki ingress                                                                                                                       |
| logging_ingress_loki_basic_auth_password      | yes       |                                              | Basic auth password for the external Loki ingress                                                                                                                       |
| logging_ingress_loki_basic_auth_password_salt |           | derived from password                        | Salt for stable bcrypt hashes — prevents unnecessary Secret updates on every run                                                                                        |
| logging_ingress_annotations                   |           | `{}`                                         | Additional annotations for the Loki ingress resource                                                                                                                    |

#### Persistent storage

Loki runs as a single-replica `StatefulSet` with a `ReadWriteOnce` PVC mounted at `/var/loki`. All data — chunks, index, WAL, and compactor state — is stored on this volume.

> **Warning:** When the PVC runs full, Loki will crash-loop. Keep `logging_loki_retention_enabled: true` and size the PVC to cover the full retention window with ~20% headroom.

#### Retention

Log retention is managed by the compactor. Expired chunks are marked during each compaction cycle and physically removed after a ~2 h grace period. This means actual disk usage decreases a few hours after the retention TTL passes.

The default retention is **30 days** (`filter-and-delete` mode), which satisfies the GDPR requirement to physically remove log data from storage. `filter-only` is not sufficient for GDPR — it only hides data from queries without deleting it.

> **Note:** Deletion is eventual. After a targeted delete request is submitted via the [Loki deletion API](https://grafana.com/docs/loki/latest/operations/storage/logs-deletion/), it takes up to ~26 h to take effect (24 h cancellation window + one compaction cycle + 2 h sweeper delay).

**Per-stream retention** lets you override the global period for specific log streams. The `selector` uses **LogQL label matchers** against the labels that Alloy attaches to every log stream (see [monitoring/logging docs](<https://metal-stack.io/docs/next/monitoring#logging> or the `Alloy` and `logging-common` roles for label overview)).

```yaml
logging_loki_retention_stream:
  # Short retention for dev namespace — matches all containers in that namespace
  - selector: '{namespace="dev"}'
    priority: 1
    period: 24h
  # Longer retention for prod namespace
  - selector: '{namespace="prod"}'
    priority: 1
    period: 720h # 30 days
  # A noisy sidecar across all namespaces — target by container name
  - selector: '{container="fluentd-sidecar"}'
    priority: 1
    period: 6h
  # More specific rule overrides the namespace rule above (higher priority wins)
  - selector: '{namespace="prod", app="ephemeral-job"}'
    priority: 2
    period: 24h
  # Keep Kubernetes events for 7 days regardless of global default
  - selector: '{job="events"}'
    priority: 1
    period: 168h
```

The highest `priority` number wins when multiple rules match a stream. Streams matching no rule fall back to `logging_loki_retention_period`.

See the [Loki retention docs](https://grafana.com/docs/loki/latest/operations/storage/retention/) for full details.

#### Monitoring

Set `logging_loki_monitoring_enabled: true` to deploy the Loki chart's built-in monitoring resources into the existing kube-prometheus-stack. Requires the [monitoring role](../monitoring/) to be deployed first.

| Resource                           | What it creates                                                |
| ---------------------------------- | -------------------------------------------------------------- |
| `ServiceMonitor`                   | Scrapes Loki metrics via Prometheus Operator                   |
| `PrometheusRule` (recording rules) | loki-mixin aggregations used by the dashboards                 |
| `PrometheusRule` (alerts)          | `LokiRequestErrors`, `LokiRequestPanics`, `LokiRequestLatency` |
| Dashboard `ConfigMaps`             | Grafana dashboards loaded automatically by the Grafana sidecar |

### Alloy

| Name                                  | Mandatory | Default                                | Description                                                                                                                            |
| ------------------------------------- | --------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_enabled                 |           | `true`                                 | Deploy Alloy. Requires `logging_alloy_chart_version` and `logging_alloy_chart_repo`.                                                   |
| logging_alloy_chart_version           |           |                                        | Helm chart version for alloy (release vector)                                                                                          |
| logging_alloy_chart_repo              |           |                                        | Repository for alloy (release vector)                                                                                                  |
| logging_alloy_cluster_label           |           | `{{ metal_control_plane_stage_name }}` | Value for the `cluster=` label on all log and metric streams. Overrides the [logging-common](../logging-common/) default.              |
| logging_alloy_service_monitor_enabled |           | `false`                                | Enable a Prometheus ServiceMonitor for Alloy self-metrics. Requires the [monitoring role](../monitoring/) to have been deployed first. |

For all other `logging_alloy_*` variables (`loki_write_endpoints`, `prometheus_write_endpoints`, WAL settings, `config_raw`), see [logging-common](../logging-common/).

### Promtail (deprecated)

| Name                           | Mandatory | Default | Description                                                                                                                                                                       |
| ------------------------------ | --------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_promtail_enabled       |           | `false` | Deploy Promtail. When `false`, any existing Promtail release is removed automatically. See [logging-common migration guide](../logging-common/README.md#migration-from-promtail). |
| logging_promtail_chart_version |           |         | Helm chart version for promtail — required when `logging_promtail_enabled: true`                                                                                                  |
| logging_promtail_chart_repo    |           |         | Repository for promtail — required when `logging_promtail_enabled: true`                                                                                                          |

## Migration from grafana/loki 5.x

This role now uses the **grafana-community/loki** Helm chart (v17+, Loki 3.x) instead of the previous `grafana/loki` v5.x (Loki 2.8.x).

**Reinstall required.** The old deployment stored logs in an `emptyDir` volume, so pod restarts already caused complete log loss. There is no data to migrate — the new chart provisions a persistent volume and starts fresh.

Key changes:

- **Persistent log storage** — logs now survive pod restarts on a PVC (the old `emptyDir` already lost everything on restart)
- **Automatic log retention** — the compactor enforces a configurable TTL (default 30 days) and physically deletes expired logs, satisfying GDPR requirements
- **Loki 3.x** — newer backend with improved performance, structured metadata support, and TSDB-based storage
- **Community-maintained chart** — the Helm chart moved to `grafana-community/loki` for ongoing maintenance

See the [upgrade guide](https://grafana.com/docs/loki/latest/setup/upgrade/upgrade-to-community/) for the full list of breaking changes across chart versions.
