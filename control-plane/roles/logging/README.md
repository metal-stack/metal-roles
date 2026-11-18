# logging

Deploys the control-plane logging stack into the Kubernetes control-plane cluster.

Components:

- **Loki** — log storage and query backend, running in [monolithic mode](https://grafana.com/docs/loki/latest/get-started/deployment-modes/#monolithic-mode) on a persistent volume
- **Alloy** — log collector (DaemonSet) via [logging-common](../logging-common/)
- Loki gateway (NGINX) with ingress, optional TLS and basic auth

Alloy is deployed by default. Existing Promtail installations are automatically removed when the role runs.
Alloy configuration, labels, meta-monitoring, and migration guidance are in [logging-common](../logging-common/).

> **Promtail is deprecated.** Setting `logging_promtail_enabled: true` emits a deprecation warning on every
> run. See the [migration guide](../logging-common/README.md#migration-from-promtail).

## Persistent storage

Loki runs as a single-replica `StatefulSet` with a `ReadWriteOnce` PVC mounted at `/var/loki`. All data — chunks, index, WAL, and compactor state — is stored on this volume.

> **Warning:** When the PVC runs full, Loki will crash-loop. Keep `logging_loki_retention_enabled: true` and size the PVC to cover the full retention window with ~20% headroom.

## Retention

Log retention is managed by the compactor. Expired chunks are marked during each compaction cycle and physically removed after a ~2 h grace period. This means actual disk usage decreases a few hours after the retention TTL passes.

The default retention is **30 days** (`filter-and-delete` mode), which satisfies the GDPR requirement to physically remove log data from storage. `filter-only` is not sufficient for GDPR — it only hides data from queries without deleting it.

> **Note:** Deletion is eventual. After a targeted delete request is submitted via the [Loki deletion API](https://grafana.com/docs/loki/latest/operations/storage/logs-deletion/), it takes up to ~26 h to take effect (24 h cancellation window + one compaction cycle + 2 h sweeper delay).

**Per-stream retention** lets you override the global period for specific log streams. The `selector` uses **LogQL label matchers** against the labels that Alloy attaches to every log stream (see [monitoring/logging docs](<https://metal-stack.io/docs/next/monitoring#logging> or the `Alloy` and `logging-common` roles for label overview)).

## Migration from grafana/loki 5.x

This role now uses the **grafana-community/loki** Helm chart (v17+, Loki 3.x) instead of the previous `grafana/loki` v5.x (Loki 2.8.x).

**Reinstall required.** The old deployment stored logs in an `emptyDir` volume only, so pod restarts caused complete log loss. There is no data to migrate.
The role can now be configured to use a persistent volume for storage, including retention.

Key changes:

- **Persistent log storage** — logs now survive pod restarts on a PVC if configured (the old `emptyDir` lost everything on restart)
- **Automatic log retention** — the compactor enforces a configurable TTL (default 30 days) and physically deletes expired logs, satisfying GDPR requirements
- **Loki 3.x** — newer backend with improved performance, structured metadata support, and TSDB-based storage
- **Community-maintained chart** — the Helm chart moved to `grafana-community/loki` for ongoing maintenance

See the [upgrade guide](https://grafana.com/docs/loki/latest/setup/upgrade/upgrade-to-community/) for the full list of breaking changes across chart versions.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/metal-roles/control-plane/roles/defaults).

```yaml
# Repository URL of the alloy helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_alloy_chart_repo: null
# Version of the alloy helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_alloy_chart_version: null
# Value for the cluster label attached to all log and metric streams.
logging_alloy_cluster_label: '{{ metal_control_plane_stage_name }}'
# Full Alloy River config override. When set, bypasses all structured vars and the template.
logging_alloy_config_raw: null
# Whether to deploy Alloy.
logging_alloy_enabled: true
# Loki push endpoints for Alloy. Each entry supports url, remote_timeout and basic_auth (username, password).
logging_alloy_loki_write_endpoints: null
# Maximum age of undelivered WAL samples before they are dropped.
logging_alloy_prometheus_wal_max_keepalive_time: null
# How often the Alloy remote_write WAL is compacted.
logging_alloy_prometheus_wal_truncate_frequency: null
# Prometheus remote_write endpoints for Alloy self-metrics.
logging_alloy_prometheus_write_endpoints: null
# Whether to create a ServiceMonitor for Alloy self-metrics scraping. Requires the monitoring role to be deployed.
logging_alloy_service_monitor_enabled: null
# Repository URL of the loki helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_chart_repo: null
# Version of the loki helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_chart_version: null
# Additional annotations for the loki ingress.
logging_ingress_annotations: {}
# Ingress DNS name of loki.
logging_ingress_dns: loki.{{ metal_control_plane_gateway_dns }}
# Basic auth password of the loki ingress.
logging_ingress_loki_basic_auth_password: null
# Salt used for generating the htpasswd entry of the loki ingress.
logging_ingress_loki_basic_auth_password_salt: null
# Basic auth user of the loki ingress.
logging_ingress_loki_basic_auth_user: promtail
# Whether TLS is enabled on the loki ingress.
logging_ingress_loki_tls: true
# Whether to deploy loki.
logging_loki_enabled: true
# Size of the loki persistent volume.
logging_loki_size: null
# The namespace to deploy the logging stack to.
logging_namespace: monitoring
# Repository URL of the promtail helm chart. Required when logging_promtail_enabled is true. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_promtail_chart_repo: null
# Version of the promtail helm chart. Required when logging_promtail_enabled is true. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
logging_promtail_chart_version: null
# Whether to deploy Promtail (deprecated). When false, any existing Promtail release is uninstalled.
logging_promtail_enabled: false
```

The highest `priority` number wins when multiple rules match a stream. The minimum value for `period` is **24h**.
Streams matching no rule fall back to `logging_loki_retention_period`.

See the [Loki retention docs](https://grafana.com/docs/loki/latest/operations/storage/retention/) for full details.
