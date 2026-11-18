# logging-common

Provides the shared Alloy DaemonSet deployment used by the [logging](../logging/) and [gardener-logging](../gardener-logging/) roles. Not intended for standalone use — it is included as a dependency by those roles.

## What Alloy does

Alloy runs as a Kubernetes DaemonSet. It:

- **Collects pod logs** from the node filesystem (`/var/log/pods`, `loki.source.file`). Pod discovery is limited to the local node via a `spec.nodeName` field selector — each DaemonSet pod only collects logs for pods scheduled on its own node. The node name is read from `K8S_NODE_NAME`, which the Alloy Helm chart injects automatically via the Kubernetes downward API.
- **Collects Kubernetes events** cluster-wide via `loki.source.kubernetes_events`. Alloy's built-in peer clustering elects a single leader — only that pod watches the events API and ships events to Loki. Without clustering every pod would independently watch the API and produce N duplicate copies in Loki.
- **Forwards everything to Loki** via `logging_common_alloy_loki_write_endpoints`.

Alloy's positions file (tracking the read offset for each log file) is persisted via a `hostPath` volume at `/var/lib/alloy/data`, so already-shipped lines are not re-read after a pod restart. The directory is created automatically on first run (`DirectoryOrCreate`).

## Labels

### Pod logs (`loki.source.file`)

| Label       | Source                                                                                                          |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| `cluster`   | `logging_common_alloy_cluster_label` (relabel rule in `discovery.relabel`)                                      |
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

| Label       | Value                                                                 |
| ----------- | --------------------------------------------------------------------- |
| `cluster`   | `logging_common_alloy_cluster_label` (relabel rule in `loki.relabel`) |
| `job`       | `events`                                                              |
| `namespace` | Namespace of the event                                                |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

`loki.source.kubernetes_events` uses Alloy's built-in clustering to elect a single leader across all DaemonSet pods — only that leader actively watches the events API and ships events to Loki. The other pods stand by and take over if the leader is restarted or evicted. Without this, every DaemonSet pod would independently watch the same events API and produce N duplicate copies in Loki (one per node). Clustering is enabled in both the River config (`clustering { enabled = true }` on the events source) and the Helm values (`alloy.clustering.enabled: true`).

## Meta-monitoring

Self-metrics are **disabled by default**. Choose one option when needed:

**Option A — Pull (ServiceMonitor).** Set `logging_alloy_service_monitor_enabled: true` (logging role) or `gardener_logging_alloy_service_monitor_enabled: true` (gardener-logging role). **Available in the logging role only** — Gardener seed Prometheus instances use annotation-based discovery restricted to extension namespaces and do not reach the `monitoring` namespace where Alloy runs.

> **Requires the monitoring role to have been deployed first.** The `ServiceMonitor` CRD is installed by kube-prometheus-stack. If it does not exist yet, Ansible fails with "no kind ServiceMonitor is registered".

**Option B — Push (remote_write).** Set `logging_alloy_prometheus_write_endpoints` (logging role) or `gardener_logging_alloy_prometheus_write_endpoints` (gardener-logging role). Works in both roles.



```yaml
{}
```

See the [monitoring role migration guide](../monitoring/README.md#thanos-receive-ingress-credentials) for credential setup.
Do not set both options simultaneously — for the logging role, `logging_alloy_service_monitor_enabled` and `logging_alloy_prometheus_write_endpoints` are mutually exclusive; for the gardener-logging role, `gardener_logging_alloy_prometheus_write_endpoints` is the only option.

### Logs

Alloy runs as a DaemonSet, so its own pod logs are captured by `loki.source.file` automatically.

## Migration from Promtail

Alloy is deployed by default by both the logging and gardener-logging roles. Existing Promtail installations are automatically removed when the roles run — no manual cleanup steps are required.

> **Promtail is deprecated.** Setting `*_promtail_enabled: true` emits a deprecation warning on every run. Promtail support will be removed in a future release.

Alloy's label derivation is identical to Promtail's, so dashboards, alerts, and LogQL queries continue to work without changes. What has changed compared to Promtail:

- **Kubernetes events are now built-in.** Alloy collects events natively via `loki.source.kubernetes_events`, labelled `job="events"`. _(logging role)_ The separate event-exporter Deployment is no longer needed — `event_exporter_enabled` defaults to `false` in the monitoring role and any existing resources are **removed automatically** when the monitoring role runs.
  > **Breaking change:** The event `job` label was renamed from `monitoring/event-exporter` to `events`. Update any existing LogQL queries, dashboard filters, and alert rules that reference `{job="monitoring/event-exporter"}` to `{job="events"}`.
- **Metric collection is now explicit.** Alloy self-metrics are disabled by default. Configure push via `logging_alloy_prometheus_write_endpoints` (logging role) or `gardener_logging_alloy_prometheus_write_endpoints` (gardener-logging role), or _(logging role only)_ pull via `logging_alloy_service_monitor_enabled`. See [Meta-monitoring](#meta-monitoring).
- **Metric WAL is new.** Alloy buffers undelivered self-metrics on disk (default: 8h). Promtail had no equivalent.

| Scenario                   | `*_alloy_enabled` | `*_promtail_enabled` | Notes                                                                                                                     |
| -------------------------- | ----------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Default**                | `true`            | `false`              | Alloy is deployed; any existing Promtail release is removed automatically.                                                |
| **Parallel run**           | `true`            | `true`               | Both collectors ship logs. Loki receives duplicate entries during this window. Deprecated — emits a warning on every run. |
| **Promtail only** (legacy) | `false`           | `true`               | Deprecated — emits a warning on every run.                                                                                |

**To migrate an existing Promtail installation:**

From the current release, Alloy is the default. Re-running the role deploys Alloy and removes Promtail automatically. _(logging role: also re-run the [monitoring](../monitoring/) role to remove the event-exporter.)_

1. If you are pushing Alloy self-metrics to Thanos Receive, migrate the credentials first — see the [monitoring role migration guide](../monitoring/README.md#thanos-receive-ingress-credentials).
2. Ensure `*_alloy_loki_write_endpoints` is set in your inventory and you have decided on a push or pull approach for self-metrics (see [Meta-monitoring](#meta-monitoring)).
3. Re-run the role _(and the [monitoring](../monitoring/) role if using the logging role)_. Alloy is deployed, the Promtail Helm release is removed, and _(logging role)_ the event-exporter resources (Deployment, ServiceAccount, ConfigMap, ClusterRole, ClusterRoleBinding) are removed automatically.
4. Verify Alloy is working: logs and Kubernetes events arrive in Loki and existing dashboards, alerts, and LogQL queries return results as expected.
5. **Optional:** Rotate the external Loki ingress credentials. The `loki-basic-auth` Kubernetes Secret is fully managed by Helm and holds a single entry derived from `logging_ingress_loki_basic_auth_user` and `logging_ingress_loki_basic_auth_password`. The default username remains `promtail` for backward compatibility — there is no need to change it. If you do want to rename the user (e.g. to `alloy`), re-running the role with updated variables replaces the secret automatically. If those credentials are also used by partition Promtail or Alloy to authenticate the `remote_write` to Loki, update both in the same deployment to avoid auth failures.

For a controlled parallel window before cutting over, set `*_promtail_enabled: true` _(and `event_exporter_enabled: true` for the logging role)_. Both collectors will ship logs — Loki receives duplicate entries during this window. Once satisfied, remove the overrides from your inventory and re-run to have Promtail and the event-exporter removed automatically.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/metal-roles/control-plane/roles/defaults).

```yaml
{}
```
