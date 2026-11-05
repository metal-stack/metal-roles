# monitoring

This role is designed to set up monitoring using Ansible.
The role includes tasks to install and configure the following monitoring tools:

- Prometheus
- Grafana
- Node Exporter
- Alertmanager

## Migration

### Thanos Receive ingress credentials

The old `monitoring_thanos_receive_ingress_basic_auth` variable (a raw htpasswd-format string) has been replaced by `monitoring_thanos_receive_ingress_basic_auth_user` and `monitoring_thanos_receive_ingress_basic_auth_password`. The htpasswd entry for nginx is now generated automatically from these, following the same pattern as Alertmanager.

> **The role will fail immediately** with a clear error message if the old variable is still set. Nothing is deployed until you migrate.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Whether the kubernetes event-exporter is deployed.
event_exporter_enabled: false
# Additional annotations for the monitoring ingresses.
monitoring_additional_ingress_annotations: {}
# Additional Alertmanager receivers.
monitoring_alertmanager_additional_receivers: []
# Additional Alertmanager routes.
monitoring_alertmanager_additional_routes: []
# Whether the Alertmanager is deployed.
monitoring_alertmanager_enabled: true
# Additional annotations for the Alertmanager ingress.
monitoring_alertmanager_ingress_annotations: {}
# Basic auth password of the Alertmanager ingress.
monitoring_alertmanager_ingress_basic_auth_password: null
# Salt used for generating the htpasswd entry of the Alertmanager ingress.
monitoring_alertmanager_ingress_basic_auth_password_salt: '{{ monitoring_alertmanager_ingress_basic_auth_password | hash(''sha1'') | truncate(22, True, '''') }}'
# Basic auth user of the Alertmanager ingress.
monitoring_alertmanager_ingress_basic_auth_user: alertmanager
# Ingress DNS name of the Alertmanager.
monitoring_alertmanager_ingress_dns: alert.{{ metal_control_plane_gateway_dns }}
# Whether to create an ingress for the Alertmanager.
monitoring_alertmanager_ingress_enabled: true
# Whether TLS is enabled on the Alertmanager ingress.
monitoring_alertmanager_ingress_tls: true
# Repeat interval for the webhook logger receiver.
monitoring_alertmanager_webhook_logger_repeat_interval: 60m
# Repeat interval for the slack receiver.
monitoring_alertmanager_webhook_slack_repeat_interval: 24h
# Whether the Gardener monitoring components are deployed. Enabled automatically when monitoring_gardener_seeds is non-empty.
monitoring_gardener_enabled: '{{ True if monitoring_gardener_seeds | length > 0 else False }}'
# The Gardener seeds to monitor.
monitoring_gardener_seeds: []
# Additional Grafana datasources.
monitoring_grafana_additional_datasources:
- access: proxy
  isDefault: false
  jsonData:
    maxLines: 1000
  name: Loki
  orgId: 1
  type: loki
  uid: loki
  url: http://loki:3100/
  version: 1
- access: proxy
  isDefault: false
  name: AlertmanagerDatasource
  orgId: 1
  type: camptocamp-prometheus-alertmanager-datasource
  uid: alertmanager-datasource
  url: http://kube-prometheus-stack-alertmanager.monitoring:9093/
  version: 1
# Admin password for Grafana.
monitoring_grafana_admin_password: admin
# Timezone used in the Grafana dashboards.
monitoring_grafana_dashboard_timezone: Europe/Berlin
# Whether Grafana and its dashboards are deployed.
monitoring_grafana_enabled: true
# Extra secret mounts for the Grafana pod.
monitoring_grafana_extra_secret_mounts: null
# GitHub OAuth configuration for Grafana (auth.github section).
monitoring_grafana_github_oauth: null
# Additional annotations for the Grafana ingress.
monitoring_grafana_ingress_annotations: {}
# Ingress DNS name of Grafana.
monitoring_grafana_ingress_dns: grafana.{{ metal_control_plane_gateway_dns }}
# Whether TLS is enabled on the Grafana ingress.
monitoring_ingress_grafana_tls: true
# The metal-api HMAC auth type used by the metal-metrics-exporter.
monitoring_metal_api_authtype: null
# The metal-api HMAC used by the metal-metrics-exporter.
monitoring_metal_api_hmac: null
# The metal-api URL scraped by the metal-metrics-exporter.
monitoring_metal_api_url: null
# The namespace to deploy the monitoring stack to.
monitoring_namespace: monitoring
# Whether CoreDNS monitoring is enabled.
monitoring_prometheus_core_dns_enabled: false
# Whether the default prometheus rules of the kube-prometheus-stack are enabled.
monitoring_prometheus_default_rules_enabled: true
# Overrides the prometheus image tag of the kube-prometheus-stack chart.
monitoring_prometheus_image_tag: null
# Ingress DNS name of Prometheus.
monitoring_prometheus_ingress_dns: prometheus.{{ metal_control_plane_gateway_dns }}
# Whether to create an ingress for Prometheus.
monitoring_prometheus_ingress_enabled: false
# Whether kube-controller-manager monitoring is enabled.
monitoring_prometheus_kube_controller_manager_enabled: false
# Whether kube-dns monitoring is enabled.
monitoring_prometheus_kube_dns_enabled: false
# Whether etcd monitoring is enabled.
monitoring_prometheus_kube_etcd_enabled: false
# Whether kube-proxy monitoring is enabled.
monitoring_prometheus_kube_proxy_enabled: false
# Service selector for the kube-proxy monitoring service.
monitoring_prometheus_kube_proxy_service_selector:
  component: kube-proxy
# Whether kube-scheduler monitoring is enabled.
monitoring_prometheus_kube_scheduler_enabled: false
# Whether kubelet monitoring is enabled.
monitoring_prometheus_kubelet_enabled: false
# Whether the prometheus operator is deployed.
monitoring_prometheus_operator_enabled: true
# Prometheus remote_write targets (name, url, username, password).
monitoring_prometheus_remote_write: []
# Storage spec (YAML string) for the prometheus statefulset.
monitoring_prometheus_storage_spec: null
# Endpoint of the metal-db used by the rethinkdb-exporter.
monitoring_rethinkdb_exporter_metal_db_endpoint: metal-db.metal-control-plane:28015
# Password of the metal-db used by the rethinkdb-exporter.
monitoring_rethinkdb_exporter_metal_db_password: change-me
# Slack webhook URL for alert notifications.
monitoring_slack_api_url: null
# Slack channel for alert notifications.
monitoring_slack_notification_channel: null
# Resource preset of the thanos compactor.
monitoring_thanos_compactor_resource_preset: medium
# Size of the thanos compactor persistent volume.
monitoring_thanos_compactor_size: 20Gi
# Storage class of the thanos compactor persistent volume.
monitoring_thanos_compactor_storage_class: null
# Whether thanos is deployed.
monitoring_thanos_enabled: true
# Thanos object store configuration (YAML string, contains credentials).
monitoring_thanos_object_store_config: null
# Probe failure threshold of the thanos object store components.
monitoring_thanos_object_store_probe_failure_threshold: 30
# Resource preset of the thanos object store components.
monitoring_thanos_object_store_resource_preset: medium
# Whether thanos receive is deployed.
monitoring_thanos_receive_enabled: false
# Additional annotations for the thanos receive ingress.
monitoring_thanos_receive_ingress_annotations: []
# Basic auth password of the thanos receive ingress.
monitoring_thanos_receive_ingress_basic_auth_password: null
# Salt used for generating the htpasswd entry of the thanos receive ingress.
monitoring_thanos_receive_ingress_basic_auth_password_salt: '{{ monitoring_thanos_receive_ingress_basic_auth_password | hash(''sha1'') | truncate(22, True, '''') }}'
# Basic auth user of the thanos receive ingress.
monitoring_thanos_receive_ingress_basic_auth_user: thanos-receive
# Ingress DNS name of thanos receive.
monitoring_thanos_receive_ingress_dns: thanos-receive.{{ metal_control_plane_gateway_dns }}
# Whether to create an ingress for thanos receive.
monitoring_thanos_receive_ingress_enabled: false
# Whether TLS is enabled on the thanos receive ingress.
monitoring_thanos_receive_ingress_tls: false
# Whether the thanos receive ingress certificate is managed by Gardener.
monitoring_thanos_receive_ingress_tls_gardener_managed: false
# Probe failure threshold of thanos receive.
monitoring_thanos_receive_probe_failure_threshold: 30
# Resource preset of thanos receive.
monitoring_thanos_receive_resource_preset: large
# Size of the thanos receive persistent volume.
monitoring_thanos_receive_size: 50Gi
# Cluster provider used by the virtual-garden-kubeconfig-refresher (one of: gcp, metalstackcloud, static). Required when Gardener monitoring is enabled.
monitoring_virtual_garden_kubeconfig_refresher_cluster_provider: null
# Whether to create local RBAC resources for accessing the garden cluster.
monitoring_virtual_garden_kubeconfig_refresher_garden_cluster_local_rbac: false
# GCP cluster name for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_gcp_cluster_name: null
# GCP location for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_gcp_location: null
# GCP project id for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_gcp_project_id: null
# metalstack.cloud API token for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_metal_stack_cloud_api_token: null
# metalstack.cloud cluster id for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_metal_stack_cloud_cluster_id: null
# metalstack.cloud project id for the virtual-garden-kubeconfig-refresher.
monitoring_virtual_garden_kubeconfig_refresher_metal_stack_cloud_project_id: null
# Static kubeconfig content for the garden cluster (cluster provider static).
monitoring_virtual_garden_kubeconfig_refresher_static_kubeconfig: null
```
