# gardener-logging

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) into Gardener shooted seeds and optionally into the garden cluster itself. Alloy collects pod logs via the Kubernetes API and forwards them to the Loki instance in the metal-stack control plane.

Expects the [logging role](../logging/) to have been deployed first.

This role supports deploying Alloy and/or Promtail as log collectors. Promtail is deployed by default for backward compatibility. See [Migration from Promtail](#migration-from-promtail) for guidance on switching to Alloy.

## Configuration

The Alloy River config is generated from structured variables at deploy time. Override individual variables to customize behavior, or bypass the template entirely with `gardener_logging_alloy_config_raw`.

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                              | Mandatory | Default | Description                                                                                                                                                                                                                    |
| ------------------------------------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| gardener_logging_alloy_enabled                    |           | `false` | Deploy Alloy. Set `true` for new installs and Alloy-only setups. Requires `gardener_logging_alloy_chart_version` and `gardener_logging_alloy_chart_repo`.                                                                      |
| gardener_logging_promtail_enabled                 |           | `true`  | Deploy Promtail (**deprecated** — see [Migration from Promtail](#migration-from-promtail)). Requires `gardener_logging_promtail_chart_version` and `gardener_logging_promtail_chart_repo`.                                     |
| gardener_logging_alloy_chart_version              |           |         | Helm chart version for alloy — required when `gardener_logging_alloy_enabled: true`                                                                                                                                            |
| gardener_logging_alloy_chart_repo                 |           |         | Repository for alloy — required when `gardener_logging_alloy_enabled: true`                                                                                                                                                    |
| gardener_logging_promtail_chart_version           |           |         | Helm chart version for promtail — required when `gardener_logging_promtail_enabled: true`                                                                                                                                      |
| gardener_logging_promtail_chart_repo              |           |         | Repository for promtail — required when `gardener_logging_promtail_enabled: true`                                                                                                                                              |
| gardener_logging_promtail_migrate_cleanup         |           | `false` | Uninstall the Promtail Helm release from the garden cluster and all shooted seeds. Set `true` after cutover to let the role remove the releases automatically. Idempotent — safe to run even if the releases are already gone. |
| gardener_logging_namespace                        |           |         | The deployment's target namespace                                                                                                                                                                                              |
| gardener_logging_ingress_dns                      |           |         | DNS for loki ingress                                                                                                                                                                                                           |
| gardener_logging_ingress_loki_basic_auth_password |           |         | The basic auth password for the external loki ingress                                                                                                                                                                          |
| gardener_logging_ingress_loki_basic_auth_user     |           |         | The basic auth user for the external loki ingress                                                                                                                                                                              |
| gardener_logging_deploy_to_garden_cluster         |           | `true`  | Deploys Alloy also into the garden cluster                                                                                                                                                                                     |
| gardener_logging_shooted_seeds                    |           |         | Shooted seed names on which to deploy Alloy that logs to loki                                                                                                                                                                  |

### Alloy

| Name                                                     | Mandatory | Default                                                                               | Description                                                                                                                                                                                                     |
| -------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_logging_alloy_port                              |           | `12345`                                                                               | Alloy listen port                                                                                                                                                                                               |
| gardener_logging_alloy_loki_write_endpoints              |           | `https://{{ gardener_logging_ingress_dns }}/loki/api/v1/push` with basic auth         | List of Loki push endpoints. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                                                  |
| gardener_logging_alloy_cluster_label                     |           | `gardener_logging_shooted_seed.name`                                                  | Value for the `cluster=` label set on all log and metric streams via relabel rules                                                                                                                              |
| gardener_logging_alloy_prometheus_write_endpoints        |           | Thanos receive ingress (`{{ monitoring_thanos_receive_ingress_dns }}/api/v1/receive`) | List of Prometheus remote_write endpoints for Alloy self-metrics. Requires `monitoring_thanos_receive_ingress_enabled: true`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` |
| gardener_logging_alloy_prometheus_wal_truncate_frequency |           | `2h`                                                                                  | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped                                                                                                                             |
| gardener_logging_alloy_prometheus_wal_max_keepalive_time |           | `8h`                                                                                  | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window                                                               |
| gardener_logging_alloy_config_raw                        |           |                                                                                       | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                          |

Alloy's positions file (tracking the read offset for each container log) is persisted via a `hostPath` volume at `/var/lib/alloy/data`. This ensures `loki.source.kubernetes` does not re-read already-shipped logs after a pod restart. The directory is created automatically on first run (`DirectoryOrCreate`).

## Labels

### Pod logs (`loki.source.kubernetes`)

| Label       | Source                                                                                                          |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| `cluster`   | `gardener_logging_alloy_cluster_label` (relabel rule in `discovery.relabel`)                                    |
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

| Label       | Value                                                                   |
| ----------- | ----------------------------------------------------------------------- |
| `cluster`   | `gardener_logging_alloy_cluster_label` (relabel rule in `loki.relabel`) |
| `job`       | `monitoring/event-exporter` (relabelled for Promtail compatibility)     |
| `namespace` | Namespace of the event                                                  |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

## Meta-monitoring

### Metrics

Alloy exposes Prometheus metrics on port `{{ gardener_logging_alloy_port }}/metrics`. Seed clusters have no local Prometheus, so metrics are pushed to the control-plane Thanos Receive ingress. The endpoint and credentials are wired automatically when `monitoring_thanos_receive_ingress_enabled: true` — credentials are taken from `monitoring_thanos_receive_ingress_basic_auth_user` and `monitoring_thanos_receive_ingress_basic_auth_password` in the monitoring role. Override `gardener_logging_alloy_prometheus_write_endpoints` only if you need custom credentials or a different URL.

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy is the recommended log collector. Promtail is deployed by default — existing installations continue to work without changes after upgrading.

> **Promtail is deprecated.** Setting `gardener_logging_promtail_enabled: true` emits a deprecation warning on every run. Promtail support will be removed in a future release.

Alloy's label derivation is identical to Promtail's, so dashboards, alerts, and LogQL queries continue to work without changes. What has changed compared to Promtail:

- **Kubernetes events are now built-in.** Promtail required a separate event-exporter Deployment. Alloy collects events natively via `loki.source.kubernetes_events` and labels them `job="monitoring/event-exporter"` for full backward compatibility.
- **Metrics are now push-based.** Promtail exposed a `/metrics` endpoint and relied on Prometheus scraping it via a ServiceMonitor. Alloy instead scrapes itself and pushes metrics via `prometheus.remote_write` to the control-plane Thanos Receive ingress, removing the ServiceMonitor ordering dependency. Wired automatically when `monitoring_thanos_receive_ingress_enabled: true`.
- **Metric WAL is new.** Alloy buffers undelivered self-metrics on disk (default: 8h). Promtail had no equivalent.

| Scenario                          | `gardener_logging_alloy_enabled` | `gardener_logging_promtail_enabled` | Notes                                                                                                                                                                         |
| --------------------------------- | -------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fresh deployment**              | `true`                           | `false`                             | Alloy only.                                                                                                                                                                   |
| **Parallel run**                  | `true`                           | `true`                              | Both DaemonSets ship logs. Loki receives duplicate entries during this window. Requires `gardener_logging_promtail_chart_version` and `gardener_logging_promtail_chart_repo`. |
| **Promtail only** (keep existing) | `false`                          | `true`                              | Promtail only. **Default behavior** — existing installs work without changes. Deprecated — emits a warning on every run.                                                      |
| **Cutover complete**              | `true`                           | `false`                             | Remove Promtail from each seed: `helm uninstall promtail -n {{ gardener_logging_namespace }}`.                                                                                |

**To migrate an existing Promtail installation:**

1. If you are pushing Alloy self-metrics to Thanos Receive, migrate the credentials first — see [Thanos Receive credentials](#thanos-receive-credentials) below.
2. Promtail runs by default and a deprecation warning fires on every run as a reminder. Proceed when ready.
3. Set `gardener_logging_alloy_enabled: true` and add `gardener_logging_alloy_chart_version` and `gardener_logging_alloy_chart_repo`. Both DaemonSets will ship logs — Loki receives duplicate entries during this window.
4. Verify Alloy is working: logs arrive in Loki and existing dashboards, alerts, and LogQL queries return results as expected.
5. Set `gardener_logging_promtail_enabled: false` and `gardener_logging_promtail_migrate_cleanup: true` and re-run. The role will uninstall the Promtail Helm release from the garden cluster and every shooted seed automatically. Remove `gardener_logging_promtail_migrate_cleanup` from your inventory afterwards.
6. Set `event_exporter_enabled: false` in your monitoring config and set `event_exporter_migrate_cleanup: true` — only needed for Promtail's event pipeline. See the [monitoring role migration guide](../monitoring/README.md#disabling-the-event-exporter-after-alloy-migration).

### Thanos Receive credentials

If you push Alloy self-metrics to Thanos Receive (`monitoring_thanos_receive_ingress_enabled: true`), the monitoring role's basic auth configuration has changed. The old raw htpasswd string `monitoring_thanos_receive_ingress_basic_auth` has been replaced by two plaintext variables:

```yaml
# Before
monitoring_thanos_receive_ingress_basic_auth: "myuser:$apr1$..."

# After
monitoring_thanos_receive_ingress_basic_auth_user: myuser # default: thanos-receive
monitoring_thanos_receive_ingress_basic_auth_password: mysecret
```

The htpasswd entry is now generated automatically. The monitoring role will fail immediately if the old variable is still set — see the [monitoring role migration guide](../monitoring/README.md#migration) for details.
