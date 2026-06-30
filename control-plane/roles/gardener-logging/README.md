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

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

### General

| Name                                              | Mandatory | Default                                      | Description                                                                                                                                                                    |
| ------------------------------------------------- | --------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| gardener_logging_alloy_enabled                    |           | `true`                                       | Deploy Alloy. Requires `gardener_logging_alloy_chart_version` and `gardener_logging_alloy_chart_repo`.                                                                         |
| gardener_logging_alloy_chart_version              |           |                                              | Helm chart version for alloy (release vector)                                                                                                                                  |
| gardener_logging_alloy_chart_repo                 |           |                                              | Repository for alloy (release vector)                                                                                                                                          |
| gardener_logging_promtail_enabled                 |           | `false`                                      | Deploy Promtail (**deprecated**). When `false`, any existing Promtail release is removed automatically from the garden cluster and all seeds. Requires chart vars when `true`. |
| gardener_logging_promtail_chart_version           |           |                                              | Helm chart version for promtail (release vector)                                                                                                                               |
| gardener_logging_promtail_chart_repo              |           |                                              | Repository for promtail (release vector)                                                                                                                                       |
| gardener_logging_namespace                        |           | `monitoring`                                 | Target namespace                                                                                                                                                               |
| gardener_logging_garden_name                      |           | `{{ gardener_defaults_garden_name }}`        | Name of the garden cluster (used as `cluster=` label for the garden cluster Alloy deployment)                                                                                  |
| gardener_logging_deploy_to_garden_cluster         |           | `true`                                       | Deploy Alloy also into the garden cluster                                                                                                                                      |
| gardener_logging_shooted_seeds                    |           | `[]`                                         | List of shooted seeds to deploy Alloy into. Each entry: `{name: <seed-name>}`                                                                                                  |
| gardener_logging_ingress_dns                      |           | `loki.{{ metal_control_plane_ingress_dns }}` | DNS for the loki ingress (used in `gardener_logging_alloy_loki_write_endpoints` examples and in the deprecated Promtail template)                                              |
| gardener_logging_ingress_loki_basic_auth_user     |           | `promtail`                                   | Basic auth user for the external loki ingress (used in `gardener_logging_alloy_loki_write_endpoints` examples and in the deprecated Promtail template)                         |
| gardener_logging_ingress_loki_basic_auth_password |           |                                              | Basic auth password for the external loki ingress. Used by the deprecated Promtail template and for configuring `gardener_logging_alloy_loki_write_endpoints`.                 |

### Alloy

| Name                                                     | Mandatory | Default | Description                                                                                                                                                                        |
| -------------------------------------------------------- | --------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_logging_alloy_loki_write_endpoints              | yes\*     | `[]`    | List of Loki push endpoints. Required when `gardener_logging_alloy_enabled: true`. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}`               |
| gardener_logging_alloy_prometheus_write_endpoints        |           | `[]`    | Prometheus remote_write endpoints for Alloy self-metrics. When empty, self-metrics are disabled. Each entry: `{url, remote_timeout?: duration, basic_auth?: {username, password}}` |
| gardener_logging_alloy_prometheus_wal_truncate_frequency |           | `2h`    | How often the WAL is compacted                                                                                                                                                     |
| gardener_logging_alloy_prometheus_wal_max_keepalive_time |           | `8h`    | Maximum time undelivered samples are kept in the WAL before being dropped                                                                                                          |
| gardener_logging_alloy_config_raw                        |           |         | Full Alloy River config override for all targets. Bypasses all structured vars and the template.                                                                                   |

All `gardener_logging_alloy_*` variables are explicitly mapped to their `logging_common_alloy_*` counterparts when calling [logging-common](../logging-common/). This is necessary because the two roles use different variable prefixes — the [logging role](../logging/) similarly maps its `logging_alloy_*` variables to `logging_common_alloy_*`.

## Migration from Promtail

See the [logging-common migration guide](../logging-common/README.md#migration-from-promtail) for general guidance.

Alloy is deployed by default. Existing Promtail installations are automatically removed from the garden cluster and all shooted seeds when the role runs.

| Scenario                   | `gardener_logging_alloy_enabled` | `gardener_logging_promtail_enabled` | Notes                                                                                                  |
| -------------------------- | -------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Default**                | `true`                           | `false`                             | Alloy is deployed; existing Promtail releases are removed automatically from all targets.              |
| **Parallel run**           | `true`                           | `true`                              | Both collectors ship logs. Loki receives duplicate entries. Deprecated — emits a warning on every run. |
| **Promtail only** (legacy) | `false`                          | `true`                              | Deprecated — emits a warning on every run.                                                             |
