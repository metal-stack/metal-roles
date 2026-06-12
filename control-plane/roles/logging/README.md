# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend
- **Alloy** — log collector (DaemonSet), collects pod logs via the Kubernetes API (`loki.source.kubernetes`) and forwards them to Loki
- Loki ingress with optional TLS and basic auth

This role supports deploying Alloy and/or Promtail as log collectors. Alloy is deployed by default. Existing Promtail installations are automatically removed when the role runs — no manual cleanup steps are required. See [Migration from Promtail](#migration-from-promtail) for details.

## Configuration

The Alloy River config is generated from structured variables at deploy time. Override individual variables to customize behavior, or bypass the template entirely with `logging_alloy_config_raw`.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                          | Mandatory | Default | Description                                                                                                                                                                                                                                                |
| --------------------------------------------- | --------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_chart_version                         | yes       |         | Helm chart version for loki (release vector)                                                                                                                                                                                                               |
| logging_chart_repo                            | yes       |         | Repository for loki (release vector)                                                                                                                                                                                                                       |
| logging_alloy_enabled                         |           | `true`  | Deploy Alloy.                                                                                                                                                                                                                                              |
| logging_promtail_enabled                      |           | `false` | Deploy Promtail (**deprecated** — see [Migration from Promtail](#migration-from-promtail)). When `false`, any existing Promtail release is removed automatically. Requires `logging_promtail_chart_version` and `logging_promtail_chart_repo` when `true`. |
| logging_alloy_chart_version                   |           |         | Helm chart version for alloy (release vector)                                                                                                                                                                                                              |
| logging_alloy_chart_repo                      |           |         | Repository for alloy (release vector)                                                                                                                                                                                                                      |
| logging_promtail_chart_version                |           |         | Helm chart version for promtail (release vector)                                                                                                                                                                                                           |
| logging_promtail_chart_repo                   |           |         | Repository for promtail (release vector)                                                                                                                                                                                                                   |
| logging_namespace                             |           |         | The deployment's target namespace                                                                                                                                                                                                                          |
| logging_loki_size                             |           |         | The size of the volume that loki will use for storing logs                                                                                                                                                                                                 |
| logging_ingress_dns                           |           |         | DNS for loki ingress                                                                                                                                                                                                                                       |
| logging_ingress_loki_tls                      |           |         | If enabled, exposes loki through HTTPS on the ingress                                                                                                                                                                                                      |
| logging_ingress_loki_basic_auth_password_salt |           |         | The basic auth password salt used for stable password hashes                                                                                                                                                                                               |
| logging_ingress_loki_basic_auth_password      |           |         | The basic auth password for the external loki ingress                                                                                                                                                                                                      |
| logging_ingress_loki_basic_auth_user          |           |         | The basic auth user for the external loki ingress                                                                                                                                                                                                          |

### Alloy

| Name                                            | Mandatory | Default                                | Description                                                                                                                                                                                                                                                                                                      |
| ----------------------------------------------- | --------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_loki_write_endpoints              |           |                                        | List of Loki push endpoints. Required when `logging_alloy_enabled: true`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                                                                                                      |
| logging_alloy_cluster_label                     |           | `{{ metal_control_plane_stage_name }}` | Value for the `cluster=` label set on all log and metric streams via relabel rules                                                                                                                                                                                                                               |
| logging_alloy_prometheus_write_endpoints        |           |                                        | List of Prometheus remote_write endpoints for Alloy self-metrics. When unset, self-metrics are disabled. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                                                                       |
| logging_alloy_service_monitor_enabled           |           | `false`                                | Enable a Prometheus ServiceMonitor for Alloy self-metrics (pull model). **The monitoring role must have been deployed first** — the `ServiceMonitor` CRD is installed by kube-prometheus-stack and must exist before this option is applied. Mutually exclusive with `logging_alloy_prometheus_write_endpoints`. |
| logging_alloy_prometheus_wal_truncate_frequency |           | `2h`                                   | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped                                                                                                                                                                                                                              |
| logging_alloy_prometheus_wal_max_keepalive_time |           | `8h`                                   | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window                                                                                                                                                                |
| logging_alloy_config_raw                        |           |                                        | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                                                                                                                           |

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

Alloy exposes Prometheus metrics on port `{{ logging_alloy_port }}/metrics`. Self-metrics are **disabled by default** — neither option below is active until explicitly configured.

**Option A — Pull (ServiceMonitor).** Set `logging_alloy_service_monitor_enabled: true`.
The recommended option when the [monitoring role](../monitoring/) is deployed on the same control-plane cluster. The role enables the Alloy ServiceMonitor and the in-cluster Prometheus scrapes `/metrics` automatically. No additional endpoint configuration is needed.

> **Requires the monitoring role to have been deployed first.** `ServiceMonitor` is a custom resource installed by the kube-prometheus-stack CRDs. If the monitoring role has not run yet, applying this option will fail immediately with a "no kind ServiceMonitor is registered" error. Deploy monitoring before logging when using this option.

**Option B — Push (remote_write).** Set `logging_alloy_prometheus_write_endpoints` to push to an external remote_write endpoint, for example the control-plane Thanos Receive ingress:

```yaml
logging_alloy_prometheus_write_endpoints:
  - url: "https://{{ monitoring_thanos_receive_ingress_dns }}/api/v1/receive"
    remote_timeout: 60s
    basic_auth:
      username: "{{ monitoring_thanos_receive_ingress_basic_auth_user }}"
      password: "{{ monitoring_thanos_receive_ingress_basic_auth_password }}"
```

See the [monitoring role migration guide](../monitoring/README.md#thanos-receive-ingress-credentials) for credential setup. Do not set both options simultaneously — `logging_alloy_service_monitor_enabled` and `logging_alloy_prometheus_write_endpoints` are mutually exclusive.

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy is the recommended log collector and is deployed by default. Existing Promtail installations are automatically removed when the logging and monitoring roles run — no manual cleanup steps are required.

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every run. Promtail support will be removed in a future release.

Alloy's label derivation is identical to Promtail's, so dashboards, alerts, and LogQL queries continue to work without changes. What has changed compared to Promtail:

- **Kubernetes events are now built-in.** Promtail required a separate event-exporter Deployment (deployed by the [monitoring role](../monitoring/)) to scrape Kubernetes events. Alloy collects events natively via `loki.source.kubernetes_events` and labels them `job="monitoring/event-exporter"` for full backward compatibility. The event-exporter is no longer needed — `event_exporter_enabled` defaults to `false` in the monitoring role, and any existing event-exporter resources are removed automatically when the monitoring role runs.
- **Metric collection is now explicit.** Promtail exposed a `/metrics` endpoint and relied on a ServiceMonitor being deployed alongside it. Alloy self-metrics are disabled by default and require an explicit choice: push via `prometheus.remote_write` (set `logging_alloy_prometheus_write_endpoints`) or pull via ServiceMonitor (set `logging_alloy_service_monitor_enabled: true`). See [Meta-monitoring](#meta-monitoring).
- **Metric WAL is new.** Alloy buffers undelivered self-metrics on disk (default: 8h). Promtail had no equivalent.

| Scenario                   | `logging_alloy_enabled` | `logging_promtail_enabled` | Notes                                                                                                                                                                                                  |
| -------------------------- | ----------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Default**                | `true`                  | `false`                    | Alloy is deployed; any existing Promtail release is removed automatically. **Default behavior.**                                                                                                       |
| **Parallel run**           | `true`                  | `true`                     | Both DaemonSets ship logs. Loki receives duplicate entries during this window. Requires `logging_promtail_chart_version` and `logging_promtail_chart_repo`. Deprecated — emits a warning on every run. |
| **Promtail only** (legacy) | `false`                 | `true`                     | Promtail only. Deprecated — emits a warning on every run.                                                                                                                                              |

**To migrate an existing Promtail installation:**

From the current release, Alloy is the default. Re-running the logging and monitoring roles deploys Alloy, removes Promtail, and removes the event-exporter automatically.

1. If you are pushing Alloy self-metrics to Thanos Receive, migrate the credentials first — see the [monitoring role migration guide](../monitoring/README.md#thanos-receive-ingress-credentials).
2. Ensure `logging_alloy_loki_write_endpoints` is set in your inventory and you have decided for a push or pull approach for self-metrics (see [Meta-monitoring](#meta-monitoring)).
3. Re-run the logging and [monitoring](../monitoring/) roles. Alloy is deployed, the Promtail Helm release is removed, and the event-exporter resources (Deployment, ServiceAccount, ConfigMap, ClusterRole, ClusterRoleBinding) are removed automatically.
4. Verify Alloy is working: logs and Kubernetes events arrive in Loki and existing dashboards, alerts, and LogQL queries return results as expected.
5. **Optional:** Rotate the external Loki ingress credentials. The `loki-basic-auth` Kubernetes Secret is fully managed by Helm and holds a single entry derived from `logging_ingress_loki_basic_auth_user` and `logging_ingress_loki_basic_auth_password`. The default username remains `promtail` for backward compatibility — there is no need to change it. If you do want to rename the user (e.g. to `alloy`), re-running the role with updated variables replaces the secret automatically. If those credentials are also used by partition Promtail or Alloy to authenticate the `remote_write` to Loki, update both in the same deployment to avoid auth failures.

If you want a controlled parallel window to verify Alloy before cutting over, set `logging_promtail_enabled: true` and `event_exporter_enabled: true`. Both DaemonSets will ship logs — Loki receives duplicate entries during this window. Once satisfied, remove the variable overrides from your inventory and re-run to have Promtail and the event-exporter removed automatically.
