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
| logging_alloy_chart_version                   | yes       | Helm chart version for alloy (release vector)                |
| logging_alloy_chart_repo                      | yes       | Repository for alloy (release vector)                        |
| logging_namespace                             |           | The deployment's target namespace                            |
| logging_loki_size                             |           | The size of the volume that loki will use for storing logs   |
| logging_ingress_dns                           |           | DNS for loki ingress                                         |
| logging_ingress_loki_tls                      |           | If enabled, exposes loki through HTTPS on the ingress        |
| logging_ingress_loki_basic_auth_password_salt |           | The basic auth password salt used for stable password hashes |
| logging_ingress_loki_basic_auth_password      |           | The basic auth password for the external loki ingress        |
| logging_ingress_loki_basic_auth_user          |           | The basic auth user for the external loki ingress            |

### Alloy

| Name                                            | Mandatory | Description                                                                                                                                                                                                                                                           |
| ----------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_chart_version                     | yes       | Helm chart version for alloy (release vector)                                                                                                                                                                                                                         |
| logging_alloy_chart_repo                        | yes       | Repository for alloy (release vector)                                                                                                                                                                                                                                 |
| logging_alloy_port                              |           | Alloy listen port (default: `12345`)                                                                                                                                                                                                                                  |
| logging_alloy_loki_write_endpoints              |           | List of Loki push endpoints. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` (default: `http://loki:3100/loki/api/v1/push`)                                                                                                         |
| logging_alloy_cluster_label                     |           | Value for the `cluster=` external label on all log streams (default: `{{ metal_control_plane_stage_name }}`)                                                                                                                                                          |
| logging_alloy_prometheus_write_endpoints        |           | List of Prometheus remote_write endpoints for Alloy self-metrics. When set, Alloy exports its own metrics via `prometheus.exporter.self` and pushes them. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` (default: `[]`, disabled) |
| logging_alloy_prometheus_wal_truncate_frequency |           | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped (default: `2h`)                                                                                                                                                                   |
| logging_alloy_prometheus_wal_max_keepalive_time |           | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window (default: `8h`)                                                                                                     |
| logging_alloy_config_raw                        |           | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                                                                                |

Alloy's positions file (tracking the read offset for each container log) is persisted via a `hostPath` volume at `/var/lib/alloy/data`. This ensures `loki.source.kubernetes` does not re-read already-shipped logs after a pod restart. The directory is created automatically on first run (`DirectoryOrCreate`).

## Labels

### Pod logs (`loki.source.kubernetes`)

| Label       | Source                                                                         |
| ----------- | ------------------------------------------------------------------------------ |
| `cluster`   | `logging_alloy_cluster_label` (external label)                                 |
| `namespace` | `__meta_kubernetes_namespace`                                                  |
| `pod`       | `__meta_kubernetes_pod_name`                                                   |
| `container` | `__meta_kubernetes_pod_container_name`                                         |
| `pod_uid`   | `__meta_kubernetes_pod_uid`                                                    |
| `node_name` | `__meta_kubernetes_pod_node_name`                                              |
| `job`       | `namespace/app` (from pod `app` label; empty suffix if pod has no `app` label) |

### Kubernetes events (`loki.source.kubernetes_events`)

| Label       | Value                                          |
| ----------- | ---------------------------------------------- |
| `cluster`   | `logging_alloy_cluster_label` (external label) |
| `job`       | `kubernetes-events`                            |
| `namespace` | Namespace of the event                         |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

## Meta-monitoring

### Metrics

Alloy exposes Prometheus metrics on port `{{ logging_alloy_port }}/metrics`. To collect them without a ServiceMonitor dependency, set `logging_alloy_prometheus_write_endpoints` — Alloy will scrape its own metrics via `prometheus.exporter.self` and push them via `prometheus.remote_write` to the configured endpoint (e.g. the in-cluster Prometheus or Thanos receive).

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy replaces Promtail as the log collector. Key differences:

| Promtail                                     | Alloy                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `config.clients[].url`                       | `logging_alloy_loki_write_endpoints[].url`                                                     |
| `-client.external-labels=cluster=…` extraArg | `logging_alloy_cluster_label` → `external_labels` in River config                              |
| `pipelineStages: [cri, docker]`              | Not needed — `loki.source.kubernetes` uses the Kubernetes API, CRI framing is already stripped |
| `pipelineStages: [match(eventrouter)]`       | `loki.source.kubernetes_events` (built-in, always enabled)                                     |

**Recommended approach — parallel run:** Deploy Alloy alongside the existing Promtail installation first. Both will ship logs to Loki simultaneously, so expect duplicate log entries during the transition window. Before removing the Promtail Helm release, verify:
- Logs arrive correctly in Loki
- Dashboards that filter by log labels (e.g. `job`, `app`) still work — the label set has changed, see [Labels](#labels)
- Alerts that query log streams by label still fire as expected
- Any custom LogQL queries saved in Grafana still return results
