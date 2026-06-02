# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend
- **Alloy** — log collector (DaemonSet), collects pod logs via the Kubernetes API (`loki.source.kubernetes`) and forwards them to Loki
- Loki ingress with optional TLS and basic auth

This role supports deploying Alloy and/or Promtail as log collectors. Promtail is deployed by default for backward compatibility. See [Migration from Promtail](#migration-from-promtail) for guidance on switching to Alloy.

## Configuration

The Alloy River config is generated from structured variables at deploy time. Override individual variables to customize behavior, or bypass the template entirely with `logging_alloy_config_raw`.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                          | Mandatory | Default | Description                                                                                                                                                                   |
| --------------------------------------------- | --------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_chart_version                         | yes       |         | Helm chart version for loki (release vector)                                                                                                                                  |
| logging_chart_repo                            | yes       |         | Repository for loki (release vector)                                                                                                                                          |
| logging_alloy_enabled                         |           | `false` | Deploy Alloy. Set `true` for new installs and Alloy-only setups. Requires `logging_alloy_chart_version` and `logging_alloy_chart_repo`.                                       |
| logging_promtail_enabled                      |           | `true`  | Deploy Promtail (**deprecated** — see [Migration from Promtail](#migration-from-promtail)). Requires `logging_promtail_chart_version` and `logging_promtail_chart_repo`.      |
| logging_alloy_chart_version                   |           |         | Helm chart version for alloy — required when `logging_alloy_enabled: true`                                                                                                    |
| logging_alloy_chart_repo                      |           |         | Repository for alloy — required when `logging_alloy_enabled: true`                                                                                                            |
| logging_promtail_chart_version                |           |         | Helm chart version for promtail — required when `logging_promtail_enabled: true`                                                                                              |
| logging_promtail_chart_repo                   |           |         | Repository for promtail — required when `logging_promtail_enabled: true`                                                                                                      |
| logging_promtail_migrate_cleanup              |           | `false` | Uninstall the Promtail Helm release. Set `true` after cutover to let the role remove the release automatically. Idempotent — safe to run even if the release is already gone. |
| logging_namespace                             |           |         | The deployment's target namespace                                                                                                                                             |
| logging_loki_size                             |           |         | The size of the volume that loki will use for storing logs                                                                                                                    |
| logging_ingress_dns                           |           |         | DNS for loki ingress                                                                                                                                                          |
| logging_ingress_loki_tls                      |           |         | If enabled, exposes loki through HTTPS on the ingress                                                                                                                         |
| logging_ingress_loki_basic_auth_password_salt |           |         | The basic auth password salt used for stable password hashes                                                                                                                  |
| logging_ingress_loki_basic_auth_password      |           |         | The basic auth password for the external loki ingress                                                                                                                         |
| logging_ingress_loki_basic_auth_user          |           |         | The basic auth user for the external loki ingress                                                                                                                             |

### Alloy

| Name                                            | Mandatory | Default                                                                         | Description                                                                                                                                         |
| ----------------------------------------------- | --------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_port                              |           | `12345`                                                                         | Alloy listen port                                                                                                                                   |
| logging_alloy_loki_write_endpoints              |           | `[{url: "http://loki:3100/loki/api/v1/push"}]`                                  | List of Loki push endpoints (in-cluster Loki). Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                    |
| logging_alloy_cluster_label                     |           | `{{ metal_control_plane_stage_name }}`                                          | Value for the `cluster=` label set on all log and metric streams via relabel rules                                                                  |
| logging_alloy_prometheus_write_endpoints        |           | auto (Thanos Receive when `monitoring_thanos_receive_enabled: true`, else `[]`) | List of Prometheus remote_write endpoints for Alloy self-metrics. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` |
| logging_alloy_prometheus_wal_truncate_frequency |           | `2h`                                                                            | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped                                                                 |
| logging_alloy_prometheus_wal_max_keepalive_time |           | `8h`                                                                            | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window   |
| logging_alloy_config_raw                        |           |                                                                                 | Full Alloy River config string override. When set, bypasses all structured vars above.                                                              |

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

| Label       | Value                                                               |
| ----------- | ------------------------------------------------------------------- |
| `cluster`   | `logging_alloy_cluster_label` (relabel rule in `loki.relabel`)      |
| `job`       | `monitoring/event-exporter` (relabelled for Promtail compatibility) |
| `namespace` | Namespace of the event                                              |

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

Alloy is the recommended log collector. Promtail is deployed by default — existing installations continue to work without changes after upgrading.

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every run. Promtail support will be removed in a future release.

Alloy's label derivation is identical to Promtail's, so dashboards, alerts, and LogQL queries continue to work without changes. What has changed compared to Promtail:

- **Kubernetes events are now built-in.** Promtail required a separate event-exporter Deployment. Alloy collects events natively via `loki.source.kubernetes_events` and labels them `job="monitoring/event-exporter"` for full backward compatibility.
- **Metrics are now push-based.** Promtail exposed a `/metrics` endpoint and relied on Prometheus scraping it via a ServiceMonitor. Alloy instead scrapes itself and pushes metrics via `prometheus.remote_write` to in-cluster Thanos Receive, removing the ServiceMonitor ordering dependency. Wired automatically when `monitoring_thanos_receive_enabled: true`.
- **Metric WAL is new.** Alloy buffers undelivered self-metrics on disk (default: 8h). Promtail had no equivalent.

| Scenario                          | `logging_alloy_enabled` | `logging_promtail_enabled` | Notes                                                                                                                                                                                                 |
| --------------------------------- | ----------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fresh deployment**              | `true`                  | `false`                    | Alloy only.                                                                                                                                                                                           |
| **Parallel run**                  | `true`                  | `true`                     | Both DaemonSets ship logs. Loki receives duplicate entries during this window. Requires `logging_promtail_chart_version` and `logging_promtail_chart_repo`.                                           |
| **Promtail only** (keep existing) | `false`                 | `true`                     | Promtail only. **Default behavior** — existing installs work without changes. Deprecated — emits a warning on every run.                                                                              |
| **Cutover complete**              | `true`                  | `false`                    | Set `logging_promtail_migrate_cleanup: true`, `event_exporter_enabled: false`, and `event_exporter_migrate_cleanup: true` (in monitoring config) and re-run. Remove the cleanup variables afterwards. |

**To migrate an existing Promtail installation:**

1. Promtail runs by default and a deprecation warning fires on every run as a reminder. Proceed when ready.
2. Set `logging_alloy_enabled: true` and add `logging_alloy_chart_version` and `logging_alloy_chart_repo`. Both DaemonSets will ship logs — Loki receives duplicate entries during this window.
3. Verify Alloy is working: logs arrive in Loki and existing dashboards, alerts, and LogQL queries return results as expected.
4. Set `logging_promtail_enabled: false` and `logging_promtail_migrate_cleanup: true` and re-run. The role will uninstall the Promtail Helm release automatically. Remove `logging_promtail_migrate_cleanup` from your inventory afterwards.
5. Set `event_exporter_enabled: false` in your monitoring config and set `event_exporter_migrate_cleanup: true` — only needed for Promtail's event pipeline. See the [monitoring role migration guide](../monitoring/README.md#disabling-the-event-exporter-after-alloy-migration).
6. Verify Promtail is removed: the DaemonSet and related resources are gone. Verify the event-exporter Deployment is removed if you also migrated that.
7. **Optional:** Rotate the external Loki ingress credentials. The `loki-basic-auth` Kubernetes Secret is fully managed by Helm and holds a single entry derived from `logging_ingress_loki_basic_auth_user` and `logging_ingress_loki_basic_auth_password`. The default username remains `promtail` for backward compatibility — there is no need to change it. If you do want to rename the user (e.g. to `alloy`), re-running the role with updated variables replaces the secret automatically. If those credentials are also used by partition Promtail or Alloy to authenticate the `remote_write` to Loki, update both in the same deployment to avoid auth failures.
