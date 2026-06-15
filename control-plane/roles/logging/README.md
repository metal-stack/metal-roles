# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend
- **Alloy** — log collector (DaemonSet) via [logging-common](../logging-common/)
- Loki ingress with optional TLS and basic auth

Alloy is deployed by default. Existing Promtail installations are automatically removed when the role runs. Alloy configuration, labels, meta-monitoring, and migration guidance are in [logging-common](../logging-common/).

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every run. See the [migration guide](../logging-common/README.md#migration-from-promtail).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). Make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

### Loki

| Name                                          | Mandatory | Default                                      | Description                                       |
| --------------------------------------------- | --------- | -------------------------------------------- | ------------------------------------------------- |
| logging_chart_version                         | yes       |                                              | Helm chart version for loki (release vector)      |
| logging_chart_repo                            | yes       |                                              | Repository for loki (release vector)              |
| logging_namespace                             |           | `monitoring`                                 | Target namespace                                  |
| logging_loki_size                             |           | `30Gi`                                       | Size of the Loki storage volume                   |
| logging_ingress_dns                           |           | `loki.{{ metal_control_plane_ingress_dns }}` | DNS for loki ingress                              |
| logging_ingress_loki_tls                      |           | `true`                                       | Expose loki through HTTPS on the ingress          |
| logging_ingress_loki_basic_auth_user          |           | `promtail`                                   | Basic auth user for the external loki ingress     |
| logging_ingress_loki_basic_auth_password      | yes       |                                              | Basic auth password for the external loki ingress |
| logging_ingress_loki_basic_auth_password_salt |           | derived from password                        | Salt for stable bcrypt password hashes            |
| logging_ingress_annotations                   |           | `{}`                                         | Additional ingress annotations                    |

### Alloy

| Name                                  | Mandatory | Default                                | Description                                                                                                                                                                                                           |
| ------------------------------------- | --------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_alloy_enabled                 |           | `true`                                 | Deploy Alloy. Requires `logging_alloy_chart_version` and `logging_alloy_chart_repo`.                                                                                                                                  |
| logging_alloy_chart_version           |           |                                        | Helm chart version for alloy (release vector)                                                                                                                                                                         |
| logging_alloy_chart_repo              |           |                                        | Repository for alloy (release vector)                                                                                                                                                                                 |
| logging_alloy_cluster_label           |           | `{{ metal_control_plane_stage_name }}` | Value for the `cluster=` label on all log and metric streams. Overrides the [logging-common](../logging-common/) default.                                                                                             |
| logging_alloy_service_monitor_enabled |           | `false`                                | Enable a Prometheus ServiceMonitor for Alloy self-metrics (pull model). **Available in this role only** — not supported in seed clusters. Requires the [monitoring role](../monitoring/) to have been deployed first. |

For all other `logging_alloy_*` variables (`loki_write_endpoints`, `prometheus_write_endpoints`, WAL settings, `config_raw`), see [logging-common](../logging-common/). Because this role and logging-common share the `logging_alloy_*` variable prefix and the role uses `import_role` (static inclusion), all `logging_alloy_*` variables set in your inventory are visible to logging-common directly — no explicit mapping is needed.

### Promtail (deprecated)

| Name                           | Mandatory | Default | Description                                                                                                                                                                       |
| ------------------------------ | --------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logging_promtail_enabled       |           | `false` | Deploy Promtail. When `false`, any existing Promtail release is removed automatically. See [logging-common migration guide](../logging-common/README.md#migration-from-promtail). |
| logging_promtail_chart_version |           |         | Helm chart version for promtail — required when `logging_promtail_enabled: true`                                                                                                  |
| logging_promtail_chart_repo    |           |         | Repository for promtail — required when `logging_promtail_enabled: true`                                                                                                          |
