# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend
- **Alloy** — log collector (DaemonSet) via [logging-common](../logging-common/)
- Loki ingress with optional TLS and basic auth

Alloy is deployed by default. Existing Promtail installations are automatically removed when the role runs. Alloy configuration, labels, meta-monitoring, and migration guidance are in [logging-common](../logging-common/).

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every run. See the [migration guide](../logging-common/README.md#migration-from-promtail).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

### Loki

| Name                                          | Mandatory | Default                                      | Description                                                                                                    |
| --------------------------------------------- | --------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| logging_chart_version                         | yes       |                                              | Helm chart version for loki (release vector)                                                                   |
| logging_chart_repo                            | yes       |                                              | Repository for loki (release vector)                                                                           |
| logging_namespace                             |           | `monitoring`                                 | Target namespace                                                                                               |
| logging_loki_size                             |           | `30Gi`                                       | Size of the Loki PVC (index, chunks, compactor scratch and ruler rules are all stored on this volume)          |
| logging_loki_storage_class                    |           | `premium-rwo`                                | StorageClass for the Loki PVC — must support `ReadWriteOnce`; use a fast block-storage class in production     |
| logging_loki_retention_enabled                |           | `true`                                       | Set to `false` to disable the compactor retention entirely — logs are kept forever.                            |
| logging_loki_retention_period                 |           | `14d`                                        | Global log retention TTL. Minimum `24h`. Only used when `logging_loki_retention_enabled` is `true`.            |
| logging_loki_deletion_mode                    |           | `filter-and-delete`                          | `filter-and-delete`: deletes from storage. `filter-only`: filters at query time only. `disabled`: no deletion. |
| logging_loki_retention_stream                 |           | `[]`                                         | Per-stream retention rules evaluated before the global period. See retention section below.                    |
| logging_ingress_dns                           |           | `loki.{{ metal_control_plane_ingress_dns }}` | DNS for loki ingress                                                                                           |
| logging_ingress_loki_tls                      |           | `true`                                       | Expose loki through HTTPS on the ingress                                                                       |
| logging_ingress_loki_basic_auth_user          |           | `promtail`                                   | Basic auth user for the external loki ingress                                                                  |
| logging_ingress_loki_basic_auth_password      | yes       |                                              | Basic auth password for the external loki ingress                                                              |
| logging_ingress_loki_basic_auth_password_salt |           | derived from password                        | Salt for stable bcrypt password hashes                                                                         |
| logging_ingress_annotations                   |           | `{}`                                         | Additional ingress annotations                                                                                 |

Loki runs as a single-binary `StatefulSet` backed by a `ReadWriteOnce` PVC mounted at `/var/loki`. All log data is stored persistently under that path.

> **Warning:** When the PVC runs full, Loki will fail to flush chunks and may crash-loop. Keep `logging_loki_retention_enabled: true` and set `logging_loki_retention_period` to a value that keeps disk usage bounded. If retention is disabled, ensure the PVC is large enough to hold logs indefinitely.

#### Retention

The compactor marks expired chunks after each compaction cycle and physically removes them after a 2h grace period. Storage usage therefore decreases with a short delay after the TTL expires.

**Sizing the PVC:** estimate daily compressed log volume × retention days, then add ~20% headroom for the compactor working directory and boltdb-shipper cache.

**Per-stream retention** can be configured via `logging_loki_retention_stream`. Rules are evaluated before the global `logging_loki_retention_period` — the highest-priority matching rule wins. Example:

```yaml
logging_loki_retention_stream:
  - selector: '{namespace="dev"}'
    priority: 1
    period: 24h
  - selector: '{namespace="prod"}'
    priority: 1
    period: 720h # 30 days
```

Since `auth_enabled: false` uses a single synthetic tenant, per-tenant overrides via `overrides.yaml` do not apply without enabling multi-tenancy.

See the [Loki 2.8 retention docs](https://archive.grafana.com/docs/loki/v2.8.x/operations/storage/retention/) and [log deletion docs](https://github.com/grafana/loki/blob/v2.8.2/docs/sources/operations/storage/logs-deletion.md) for full configuration options.

### Alloy

| Name                                  | Mandatory | Default                                | Description                                                                                                                                                                                                           |
| ------------------------------------- | --------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_enabled                 |           | `true`                                 | Deploy Alloy. Requires `logging_alloy_chart_version` and `logging_alloy_chart_repo`.                                                                                                                                  |
| logging_alloy_chart_version           |           |                                        | Helm chart version for alloy (release vector)                                                                                                                                                                         |
| logging_alloy_chart_repo              |           |                                        | Repository for alloy (release vector)                                                                                                                                                                                 |
| logging_alloy_cluster_label           |           | `{{ metal_control_plane_stage_name }}` | Value for the `cluster=` label on all log and metric streams. Overrides the [logging-common](../logging-common/) default.                                                                                             |
| logging_alloy_service_monitor_enabled |           | `false`                                | Enable a Prometheus ServiceMonitor for Alloy self-metrics (pull model). **Available in this role only** — not supported in seed clusters. Requires the [monitoring role](../monitoring/) to have been deployed first. |

For all other `logging_alloy_*` variables (`loki_write_endpoints`, `prometheus_write_endpoints`, WAL settings, `config_raw`), see [logging-common](../logging-common/). All `logging_alloy_*` variables set in your inventory are explicitly mapped to their `logging_common_alloy_*` counterparts when calling logging-common.

### Promtail (deprecated)

| Name                           | Mandatory | Default | Description                                                                                                                                                                       |
| ------------------------------ | --------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_promtail_enabled       |           | `false` | Deploy Promtail. When `false`, any existing Promtail release is removed automatically. See [logging-common migration guide](../logging-common/README.md#migration-from-promtail). |
| logging_promtail_chart_version |           |         | Helm chart version for promtail — required when `logging_promtail_enabled: true`                                                                                                  |
| logging_promtail_chart_repo    |           |         | Repository for promtail — required when `logging_promtail_enabled: true`                                                                                                          |
