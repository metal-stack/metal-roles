# gardener-logging

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) into Gardener shooted seeds and optionally into the garden cluster itself. Alloy collects pod logs via the Kubernetes API and forwards them to the Loki instance in the metal-stack control plane.

Expects the [logging role](../logging/) to have been deployed first.

This role supports deploying Alloy and/or Promtail as log collectors. Promtail is deployed by default for backward compatibility. See [Migration from Promtail](#migration-from-promtail) for guidance on switching to Alloy.

## Background and Architecture

### Why this role exists

Gardener ships with a built-in logging stack — gardenlet can deploy [Vali](https://github.com/credativ/plutono) (a Loki fork) and fluent-bit into each seed cluster. The metal-stack deployment disables this stack intentionally.

Instead, this role deploys Alloy as a DaemonSet into the Garden cluster and Shooted Seeds to ship **all** pod logs to the central Loki instance in the metal-stack control plane. This gives platform operators a single place to query infrastructure logs across all Gardener clusters — including the Garden cluster itself, seed system components, and extension controllers.

This role targets the **Garden cluster** (`gardener_logging_deploy_to_garden_cluster: true`) and **Shooted Seeds** (`gardener_logging_shooted_seeds`).

### Why there are two task files

- **`tasks/main.yaml`** — handles the Garden cluster. The Garden cluster is a normal Kubernetes cluster reachable with the current kubeconfig. Alloy is deployed directly.
- **`tasks/gardener-shooted-seed.yaml`** — handles one Shooted Seed per loop iteration. Because Shooted Seeds are managed as Shoots, their kubeconfig is not directly available. The task fetches it via the virtual garden API (`virtual_garden_kubeconfig` + `shoot_admin_kubeconfig` filter), then deploys Alloy using that kubeconfig.

### What gets collected

Alloy runs as a Kubernetes DaemonSet in the `monitoring` namespace. It uses `loki.source.kubernetes` to collect logs from **every pod** in the cluster via the Kubernetes API — no annotations, opt-in labels, or per-service configuration is required. Kubernetes events are also collected natively via `loki.source.kubernetes_events`.

### Prometheus metrics

Alloy can optionally push its own self-metrics to a remote Prometheus endpoint (see [Meta-monitoring](#meta-monitoring)). It does **not** collect metrics from other workloads in the cluster.

Seed workload metrics are Gardener's responsibility: gardenlet manages Cache, Seed, and Aggregate Prometheus instances on each seed. Those Prometheus instances use annotation-based discovery restricted to known namespaces and do not reach the `monitoring` namespace where Alloy runs — pull-based metric collection from Alloy is therefore not supported.

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

| Name                                                     | Mandatory | Default                              | Description                                                                                                                                                                                                                                                             |
| -------------------------------------------------------- | --------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_logging_alloy_port                              |           | `12345`                              | Alloy listen port                                                                                                                                                                                                                                                       |
| gardener_logging_alloy_loki_write_endpoints              |           |                                      | List of Loki push endpoints. Required when `gardener_logging_alloy_enabled: true`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                                                    |
| gardener_logging_alloy_cluster_label                     |           | `gardener_logging_shooted_seed.name` | Value for the `cluster=` label set on all log and metric streams via relabel rules. Defaults to the shooted seed name per loop iteration; the garden cluster deployment substitutes `gardener_logging_garden_name` via task-level vars before the template is rendered. |
| gardener_logging_alloy_prometheus_write_endpoints        |           |                                      | List of Prometheus remote_write endpoints for Alloy self-metrics. When unset, self-metrics are disabled. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                                                              |
| gardener_logging_alloy_prometheus_wal_truncate_frequency |           | `2h`                                 | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped                                                                                                                                                                                     |
| gardener_logging_alloy_prometheus_wal_max_keepalive_time |           | `8h`                                 | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window                                                                                                                       |
| gardener_logging_alloy_config_raw                        |           |                                      | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                                                                                  |

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

| Label       | Value                                                                                |
| ----------- | ------------------------------------------------------------------------------------ |
| `cluster`   | `gardener_logging_alloy_cluster_label` (relabel rule in `loki.relabel`)              |
| `job`       | `monitoring/event-exporter` — stream name used consistently across all logging roles |
| `namespace` | Namespace of the event                                                               |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

## Meta-monitoring

### Metrics

Alloy exposes Prometheus metrics on port `{{ gardener_logging_alloy_port }}/metrics`. Self-metrics are disabled by default.

Alloy can scrape itself and push metrics to a remote_write endpoint. This works regardless of the Prometheus setup on the seed. The target just needs to support remote_write.
Set `gardener_logging_alloy_prometheus_write_endpoints` to push to a remote_write endpoint.

Example for Thanos Receive ingress:

```yaml
gardener_logging_alloy_prometheus_write_endpoints:
  - url: "https://{{ monitoring_thanos_receive_ingress_dns }}/api/v1/receive"
    remote_timeout: 60s
    basic_auth:
      username: "{{ monitoring_thanos_receive_ingress_basic_auth_user }}"
      password: "{{ monitoring_thanos_receive_ingress_basic_auth_password }}"
```

Gardener's Prometheus instances use annotation-based pod discovery restricted to extension namespaces (Seed Prometheus) or scrape their own known targets (Aggregate Prometheus). Neither reliably reaches the `monitoring` namespace where Alloy runs, so pull-based collection is not a supported option.

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy is the recommended log collector. Promtail is deployed by default — existing installations continue to work without changes after upgrading.

> **Promtail is deprecated.** Setting `gardener_logging_promtail_enabled: true` emits a deprecation warning on every run. Promtail support will be removed in a future release.

Alloy's label derivation is identical to Promtail's, so dashboards, alerts, and LogQL queries continue to work without changes. What has changed compared to Promtail:

- **Kubernetes events are now built-in.** The previous Promtail deployment in this role only collected pod logs (`cri`/`docker` pipeline stages) — it had no event collection at all. Alloy adds native Kubernetes event collection via `loki.source.kubernetes_events`, labelled `job="monitoring/event-exporter"` for consistency with the control-plane logging role.
- **Metrics are now push-based.** Promtail exposed a `/metrics` endpoint and relied on Prometheus scraping it via a ServiceMonitor. Alloy instead scrapes itself and pushes metrics via `prometheus.remote_write`, removing the ServiceMonitor ordering dependency. Configure `gardener_logging_alloy_prometheus_write_endpoints` to enable this — see [Meta-monitoring](#meta-monitoring).
- **Metric WAL is new.** Alloy buffers undelivered self-metrics on disk (default: 8h). Promtail had no equivalent.

| Scenario                          | `gardener_logging_alloy_enabled` | `gardener_logging_promtail_enabled` | Notes                                                                                                                                                                                                     |
| --------------------------------- | -------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fresh deployment**              | `true`                           | `false`                             | Alloy only.                                                                                                                                                                                               |
| **Parallel run**                  | `true`                           | `true`                              | Both DaemonSets ship logs. Loki receives duplicate entries during this window. Requires `gardener_logging_promtail_chart_version` and `gardener_logging_promtail_chart_repo`.                             |
| **Promtail only** (keep existing) | `false`                          | `true`                              | Promtail only. **Default behavior** — existing installs work without changes. Deprecated — emits a warning on every run.                                                                                  |
| **Cutover complete**              | `true`                           | `false`                             | Set `gardener_logging_promtail_migrate_cleanup: true` and re-run. The role removes the Promtail Helm release from the garden cluster and all shooted seeds automatically. Remove the variable afterwards. |

**To migrate an existing Promtail installation:**

1. If you are pushing Alloy self-metrics to Thanos Receive, migrate the credentials first — see the [monitoring role migration guide](../monitoring/README.md#thanos-receive-ingress-credentials).
2. Promtail runs by default and a deprecation warning fires on every run as a reminder. Proceed when ready.
3. Set `gardener_logging_alloy_enabled: true` and add `gardener_logging_alloy_chart_version` and `gardener_logging_alloy_chart_repo`. Both DaemonSets will ship logs — Loki receives duplicate entries during this window.
4. Verify Alloy is working: logs arrive in Loki and existing dashboards, alerts, and LogQL queries return results as expected.
5. Set `gardener_logging_promtail_enabled: false` and `gardener_logging_promtail_migrate_cleanup: true` and re-run. The role will uninstall the Promtail Helm release from the garden cluster and every shooted seed automatically. Remove `gardener_logging_promtail_migrate_cleanup` from your inventory afterwards.
6. Verify Promtail is removed: the DaemonSet and related resources are gone.
7. **Optional:** Rotate the external Loki ingress credentials. The `loki-basic-auth` Kubernetes Secret is fully managed by Helm and holds a single entry derived from `logging_ingress_loki_basic_auth_user` and `logging_ingress_loki_basic_auth_password`. The default username remains `promtail` for backward compatibility — there is no need to change it. If you do want to rename the user (e.g. to `alloy`), re-running the logging role with updated variables replaces the secret automatically. If those credentials are also configured in `gardener_logging_ingress_loki_basic_auth_user` / `gardener_logging_ingress_loki_basic_auth_password` for Alloy/Promtail on the shooted seeds, update all of them in the same deployment to avoid auth failures.
