# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend
- **Alloy** — log collector (DaemonSet), collects pod logs via the Kubernetes API (`loki.source.kubernetes`) and forwards them to Loki
- Loki ingress with optional TLS and basic auth

This role previously used Promtail as the log collector. It has been migrated to use Grafana Alloy instead. See [Migration from Promtail](#migration-from-promtail) for details.

## Configuration

The Alloy River config is generated from structured variables at deploy time. Override individual variables to customize behavior, or bypass the template entirely with `logging_alloy_config_raw`.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                          | Mandatory | Description                                                  |
| --------------------------------------------- | --------- | ------------------------------------------------------------ |
| logging_chart_version                         | yes       | Helm chart version for loki (release vector)                 |
| logging_chart_repo                            | yes       | Repository for loki (release vector)                         |
| logging_alloy_chart_version                   |           | Helm chart version for alloy — deploy Alloy when set         |
| logging_alloy_chart_repo                      |           | Repository for alloy                                         |
| logging_promtail_chart_version                |           | Helm chart version for promtail — deploy Promtail when set   |
| logging_promtail_chart_repo                   |           | Repository for promtail                                      |
| logging_namespace                             |           | The deployment's target namespace                            |
| logging_loki_size                             |           | The size of the volume that loki will use for storing logs   |
| logging_ingress_dns                           |           | DNS for loki ingress                                         |
| logging_ingress_loki_tls                      |           | If enabled, exposes loki through HTTPS on the ingress        |
| logging_ingress_loki_basic_auth_password_salt |           | The basic auth password salt used for stable password hashes |
| logging_ingress_loki_basic_auth_password      |           | The basic auth password for the external loki ingress        |
| logging_ingress_loki_basic_auth_user          |           | The basic auth user for the external loki ingress            |

### Alloy

| Name                                            | Mandatory | Description                                                                                                                                                                                                                                                       |
| ----------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_chart_version                     |           | Helm chart version for alloy. Alloy is deployed only when this is set.                                                                                                                                                                                            |
| logging_alloy_chart_repo                        |           | Repository for alloy                                                                                                                                                                                                                                              |
| logging_alloy_port                              |           | Alloy listen port (default: `12345`)                                                                                                                                                                                                                              |
| logging_alloy_loki_write_endpoints              |           | List of Loki push endpoints. Default: `[{url: "http://loki:3100/loki/api/v1/push"}]` (in-cluster Loki). Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                         |
| logging_alloy_cluster_label                     |           | Value for the `cluster=` label set on all log and metric streams via relabel rules (default: `{{ metal_control_plane_stage_name }}`)                                                                                                                              |
| logging_alloy_prometheus_write_endpoints        |           | List of Prometheus remote_write endpoints for Alloy self-metrics. Auto-populated with in-cluster Thanos Receive when `monitoring_thanos_receive_enabled: true`, otherwise `[]`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` |
| logging_alloy_prometheus_wal_truncate_frequency |           | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped (default: `2h`)                                                                                                                                                               |
| logging_alloy_prometheus_wal_max_keepalive_time |           | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window (default: `8h`)                                                                                                 |
| logging_alloy_config_raw                        |           | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                                                                            |

Alloy's positions file (tracking the read offset for each container log) is persisted via a `hostPath` volume at `/var/lib/alloy/data`. This ensures `loki.source.kubernetes` does not re-read already-shipped logs after a pod restart. The directory is created automatically on first run (`DirectoryOrCreate`).

## Labels

### Pod logs (`loki.source.kubernetes`)

| Label       | Source                                                                                                          |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| `cluster`   | `logging_alloy_cluster_label` (relabel rule in `discovery.relabel`)                                             |
| `namespace` | `__meta_kubernetes_namespace`                                                                                   |
| `pod`       | `__meta_kubernetes_pod_name`                                                                                    |
| `container` | `__meta_kubernetes_pod_container_name`                                                                          |
| `pod_uid`   | `__meta_kubernetes_pod_uid`                                                                                     |
| `node_name` | `__meta_kubernetes_pod_node_name`                                                                               |
| `app`       | `app.kubernetes.io/name` pod label, falling back to `app` label, controller name (hash stripped), then pod name |
| `instance`  | `app.kubernetes.io/instance` pod label, falling back to `instance` label (empty if neither is set)              |
| `component` | `app.kubernetes.io/component` pod label, falling back to `component` label (empty if neither is set)            |
| `job`       | `namespace/app` (using the computed `app` value above)                                                          |

### Kubernetes events (`loki.source.kubernetes_events`)

| Label       | Value                                                          |
| ----------- | -------------------------------------------------------------- |
| `cluster`   | `logging_alloy_cluster_label` (relabel rule in `loki.relabel`) |
| `job`       | `kubernetes-events`                                            |
| `namespace` | Namespace of the event                                         |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

## Meta-monitoring

### Metrics

Alloy exposes Prometheus metrics on port `{{ logging_alloy_port }}/metrics`. When `monitoring_thanos_receive_enabled: true` in the monitoring role, Alloy automatically pushes metrics to the in-cluster Thanos Receive. Otherwise the list is empty and self-metrics are disabled. Override to customise:

```yaml
logging_alloy_prometheus_write_endpoints:
  # automatically included when monitoring_thanos_receive_enabled: true
  - url: "http://thanos-receive.{{ logging_namespace }}.svc.cluster.local:19291/api/v1/receive"
```

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy is the recommended log collector for new installations. Existing installations can migrate at their own pace — both Promtail and Alloy can run in parallel, though this will produce duplicate log entries in Loki for the duration.

What has changed compared to Promtail:

- **Log labels are consistent with Promtail.** The label derivation rules (`app`, `instance`, `component`, `job`) are identical to Promtail's chart defaults. The only addition is `pod_uid`. See [Labels](#labels) for the full set.
- **Kubernetes events are now built-in.** Promtail required a separate `eventrouter` sidecar and a pipeline stage to capture events. Alloy collects events natively via `loki.source.kubernetes_events`. Events now appear under `job="kubernetes-events"` instead of `job="monitoring/event-exporter"` — update any queries or dashboards accordingly.
- **Alloy pushes its own metrics.** Promtail exposed metrics, but enabling the ServiceMonitor was impractical because Prometheus typically deploys after the logging stack (the option was intentionally commented out). Alloy scrapes itself and pushes metrics via `prometheus.remote_write` instead, removing the ordering dependency. When `monitoring_thanos_receive_enabled: true`, this is wired automatically.
- **Metric WAL is new.** Alloy buffers undelivered self-metrics in a WAL on disk (default retention: 8h). Promtail had no equivalent — if Loki was unreachable, metric data was simply lost.

**To migrate an existing installation:**

1. Add `logging_alloy_chart_version` and `logging_alloy_chart_repo` to your config alongside the existing Promtail vars. Both will run in parallel — Loki will receive duplicate log entries during this window.
2. Before removing Promtail, verify:

- Logs arrive correctly in Loki
- Dashboards and alerts that filter by log labels work as expected — labels are consistent with Promtail
- Any custom LogQL queries saved in Grafana still return results
