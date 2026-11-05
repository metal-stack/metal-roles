# gardener-logging

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) into Gardener shooted seeds and optionally into the garden cluster itself. Alloy reads pod logs from the node filesystem and forwards them to the Loki instance in the metal-stack control plane.

Expects the [logging role](../logging/) to have been deployed first.

Alloy configuration, labels, meta-monitoring, and migration guidance are documented in [logging-common](../logging-common/).

> **Promtail is deprecated.** Setting `gardener_logging_promtail_enabled: true` emits a deprecation warning on every run. See the [migration guide](../logging-common/README.md#migration-from-promtail).

## Background and Architecture

### Why this role exists

Gardener ships with a built-in logging stack — gardenlet can deploy [Vali](https://github.com/credativ/plutono) (a Loki fork) and fluent-bit into each seed cluster. The metal-stack deployment disables this stack intentionally.

Instead, this role deploys Alloy as a DaemonSet into the Garden cluster and Shooted Seeds to ship **all** pod logs to the central Loki instance in the metal-stack control plane. This gives platform operators a single place to query infrastructure logs across all Gardener clusters — including the Garden cluster itself, seed system components, and extension controllers.

This role targets the **Garden cluster** (`gardener_logging_deploy_to_garden_cluster: true`) and **Shooted Seeds** (`gardener_logging_shooted_seeds`).

### Why there are two task files

- **`tasks/main.yaml`** — handles the Garden cluster. The Garden cluster is a normal Kubernetes cluster reachable with the current kubeconfig. Alloy is deployed directly.
- **`tasks/gardener-shooted-seed.yaml`** — handles one Shooted Seed per loop iteration. Because Shooted Seeds are managed as Shoots, their kubeconfig is not directly available. The task fetches it via the virtual garden API (`virtual_garden_kubeconfig` + `shoot_admin_kubeconfig` filter), then deploys Alloy using that kubeconfig.

### What gets collected

Alloy runs as a Kubernetes DaemonSet in the `monitoring` namespace. It reads pod logs from the node filesystem (`/var/log/pods`, `loki.source.file`) — one DaemonSet pod per node, collecting only the logs for pods scheduled on that node. Kubernetes events are also collected natively via `loki.source.kubernetes_events` with clustering-based leader election to avoid duplication.

### Prometheus metrics

Alloy can optionally push its own self-metrics to a remote Prometheus endpoint (see [logging-common meta-monitoring](../logging-common/README.md#meta-monitoring)). It does **not** collect metrics from other workloads in the cluster.

Seed workload metrics are Gardener's responsibility: gardenlet manages Cache, Seed, and Aggregate Prometheus instances on each seed. Those Prometheus instances use annotation-based discovery restricted to known namespaces and do not reach the `monitoring` namespace where Alloy runs — pull-based metric collection from Alloy is not supported. Use push via `logging_alloy_prometheus_write_endpoints` instead.

## Migration from Promtail

See the [logging-common migration guide](../logging-common/README.md#migration-from-promtail) for general guidance.

Alloy is deployed by default. Existing Promtail installations are automatically removed from the garden cluster and all shooted seeds when the role runs.

| Scenario                   | `gardener_logging_alloy_enabled` | `gardener_logging_promtail_enabled` | Notes                                                                                                  |
| -------------------------- | -------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Default**                | `true`                           | `false`                             | Alloy is deployed; existing Promtail releases are removed automatically from all targets.              |
| **Parallel run**           | `true`                           | `true`                              | Both collectors ship logs. Loki receives duplicate entries. Deprecated — emits a warning on every run. |
| **Promtail only** (legacy) | `false`                          | `true`                              | Deprecated — emits a warning on every run.                                                             |

## Variables

All `gardener_logging_alloy_*` variables are explicitly mapped to their `logging_common_alloy_*` counterparts when calling [logging-common](../logging-common/). This is necessary because the two roles use different variable prefixes — the [logging role](../logging/) similarly maps its `logging_alloy_*` variables to `logging_common_alloy_*`.

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Repository URL of the alloy helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
gardener_logging_alloy_chart_repo: null
# Version of the alloy helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
gardener_logging_alloy_chart_version: null
# Whether to deploy Alloy.
gardener_logging_alloy_enabled: true
# Loki push endpoints for Alloy. Each entry supports url, remote_timeout and basic_auth (username, password).
gardener_logging_alloy_loki_write_endpoints: []
# Maximum age of undelivered WAL samples before they are dropped.
gardener_logging_alloy_prometheus_wal_max_keepalive_time: 8h
# How often the Alloy remote_write WAL is compacted.
gardener_logging_alloy_prometheus_wal_truncate_frequency: 2h
# Prometheus remote_write endpoints for Alloy self-metrics.
gardener_logging_alloy_prometheus_write_endpoints: []
# Whether to deploy Alloy to the garden cluster.
gardener_logging_deploy_to_garden_cluster: true
# Name of the garden.
gardener_logging_garden_name: '{{ gardener_defaults_garden_name }}'
# Ingress DNS name of loki.
gardener_logging_ingress_dns: loki.{{ metal_control_plane_gateway_dns }}
# Basic auth password of the loki ingress.
gardener_logging_ingress_loki_basic_auth_password: null
# Basic auth user of the loki ingress.
gardener_logging_ingress_loki_basic_auth_user: promtail
# The namespace to deploy the logging components to.
gardener_logging_namespace: monitoring
# Repository URL of the promtail helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
gardener_logging_promtail_chart_repo: null
# Version of the promtail helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
gardener_logging_promtail_chart_version: null
# Whether to deploy Promtail (deprecated). Requires gardener_logging_promtail_chart_version and gardener_logging_promtail_chart_repo when enabled.
gardener_logging_promtail_enabled: false
# The shooted seeds to deploy the logging components to.
gardener_logging_shooted_seeds: []
```
