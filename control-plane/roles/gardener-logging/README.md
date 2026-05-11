# gardener-logging

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) into Gardener shooted seeds and optionally into the garden cluster itself. Alloy collects pod logs via the Kubernetes API and forwards them to the Loki instance in the metal-stack control plane.

Expects the [logging role](../logging/) to have been deployed first.

This role previously used Promtail as the log collector. It has been migrated to use Grafana Alloy instead. See [Migration from Promtail](#migration-from-promtail) for details.

## Configuration

The Alloy River config is generated from structured variables at deploy time. Override individual variables to customize behavior, or bypass the template entirely with `gardener_logging_alloy_config_raw`.

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                              | Mandatory | Description                                                   |
| ------------------------------------------------- | --------- | ------------------------------------------------------------- |
| gardener_logging_alloy_chart_version              | yes       | Helm chart version for alloy (release vector)                 |
| gardener_logging_alloy_chart_repo                 | yes       | Repository for alloy (release vector)                         |
| gardener_logging_namespace                        |           | The deployment's target namespace                             |
| gardener_logging_ingress_dns                      |           | DNS for loki ingress                                          |
| gardener_logging_ingress_loki_basic_auth_password |           | The basic auth password for the external loki ingress         |
| gardener_logging_ingress_loki_basic_auth_user     |           | The basic auth user for the external loki ingress             |
| gardener_logging_deploy_to_garden_cluster         |           | Deploys Alloy also into the garden cluster (default: `true`)  |
| gardener_logging_shooted_seeds                    |           | Shooted seed names on which to deploy Alloy that logs to loki |

### Alloy

| Name                                                     | Mandatory | Description                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_logging_alloy_chart_version                     | yes       | Helm chart version for alloy (release vector)                                                                                                                                                                                                                                                                   |
| gardener_logging_alloy_chart_repo                        | yes       | Repository for alloy (release vector)                                                                                                                                                                                                                                                                           |
| gardener_logging_alloy_port                              |           | Alloy listen port (default: `12345`)                                                                                                                                                                                                                                                                            |
| gardener_logging_alloy_loki_write_endpoints              |           | List of Loki push endpoints. Default: `https://{{ gardener_logging_ingress_dns }}/loki/api/v1/push` with `basic_auth` using `gardener_logging_ingress_loki_basic_auth_user/password`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`                                         |
| gardener_logging_alloy_cluster_label                     |           | Value for the `cluster=` external label on all log streams (default: `gardener_logging_shooted_seed.name`)                                                                                                                                                                                                      |
| gardener_logging_alloy_prometheus_write_endpoints        |           | List of Prometheus remote_write endpoints for Alloy self-metrics. Default: Thanos receive ingress (`{{ monitoring_thanos_receive_ingress_dns }}/api/v1/receive`). Requires `monitoring_thanos_receive_ingress_enabled: true`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` |
| gardener_logging_alloy_prometheus_wal_truncate_frequency |           | How often the WAL is compacted. Samples older than `max_keepalive_time` are dropped (default: `2h`)                                                                                                                                                                                                             |
| gardener_logging_alloy_prometheus_wal_max_keepalive_time |           | Maximum time undelivered samples are kept in the WAL before being dropped. Increase if you expect remote endpoint outages longer than this window (default: `8h`)                                                                                                                                               |
| gardener_logging_alloy_config_raw                        |           | Full Alloy River config string override. When set, bypasses all structured vars above.                                                                                                                                                                                                                          |

Alloy's positions file (tracking the read offset for each container log) is persisted via a `hostPath` volume at `/var/lib/alloy/data`. This ensures `loki.source.kubernetes` does not re-read already-shipped logs after a pod restart. The directory is created automatically on first run (`DirectoryOrCreate`).

## Labels

### Pod logs (`loki.source.kubernetes`)

| Label       | Source                                                                         |
| ----------- | ------------------------------------------------------------------------------ |
| `cluster`   | `gardener_logging_alloy_cluster_label` (external label)                        |
| `namespace` | `__meta_kubernetes_namespace`                                                  |
| `pod`       | `__meta_kubernetes_pod_name`                                                   |
| `container` | `__meta_kubernetes_pod_container_name`                                         |
| `pod_uid`   | `__meta_kubernetes_pod_uid`                                                    |
| `node_name` | `__meta_kubernetes_pod_node_name`                                              |
| `app`       | `__meta_kubernetes_pod_label_app` (empty if pod has no `app` label)            |
| `job`       | `namespace/app` (from pod `app` label; empty suffix if pod has no `app` label) |

### Kubernetes events (`loki.source.kubernetes_events`)

| Label       | Value                                                   |
| ----------- | ------------------------------------------------------- |
| `cluster`   | `gardener_logging_alloy_cluster_label` (external label) |
| `job`       | `kubernetes-events`                                     |
| `namespace` | Namespace of the event                                  |

Alloy watches events in all namespaces, which requires cluster-scope RBAC. The Alloy Helm chart includes the required `events` rule in its default `rbac.rules`, so no additional configuration is needed.

## Meta-monitoring

### Metrics

Alloy exposes Prometheus metrics on port `{{ gardener_logging_alloy_port }}/metrics`. Seed clusters have no local Prometheus, so metrics are pushed to the control-plane Thanos Receive ingress. The endpoint and credentials are wired automatically when `monitoring_thanos_receive_ingress_enabled: true` — credentials are taken from `monitoring_thanos_receive_ingress_basic_auth_user` and `monitoring_thanos_receive_ingress_basic_auth_password` in the monitoring role. Override `gardener_logging_alloy_prometheus_write_endpoints` only if you need custom credentials or a different URL.

### Logs

Alloy runs as a Kubernetes DaemonSet, so its own pod logs are captured by `loki.source.kubernetes` automatically — no additional configuration is needed.

## Migration from Promtail

Alloy replaces Promtail as the log collector. Key differences:

| Promtail                                     | Alloy                                                                      |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| `config.clients[].url` + `basic_auth`        | `gardener_logging_alloy_loki_write_endpoints[].url` + `basic_auth`         |
| `-client.external-labels=cluster=…` extraArg | `gardener_logging_alloy_cluster_label` → `external_labels` in River config |
| `pipelineStages: [cri, docker]`              | Not needed — `loki.source.kubernetes` uses the Kubernetes API              |

**Recommended approach — parallel run:** Deploy Alloy alongside the existing Promtail installation first. Both will ship logs to Loki simultaneously, so expect duplicate log entries during the transition window. Before removing the Promtail Helm releases, verify:

- Logs arrive correctly in Loki
- Dashboards that filter by log labels (e.g. `job`, `app`) still work — the label set has changed, see [Labels](#labels)
- Alerts that query log streams by label still fire as expected
- Any custom LogQL queries saved in Grafana still return results
