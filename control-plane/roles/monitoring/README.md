# monitoring

This role is designed to set up monitoring using Ansible.
The role includes tasks to install and configure the following monitoring tools:

- Prometheus
- Grafana
- Node Exporter
- Alertmanager

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).
The following variables can be set to configure the role:

### General

| Name                                          | Mandatory | Description                                                                                                                                                     |
|-----------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rethinkdb_exporter_name                       | yes       | rethinkdb exporter image name                                                                                                                                   |
| rethinkdb_exporter_tag                        | yes       | rethinkdb exporter image tag                                                                                                                                    |
| event_exporter_name                           | yes       | event exporter image name                                                                                                                                       |
| event_exporter_tag                            | yes       | event exporter image tag                                                                                                                                        |
| prometheus_chart_version                      | yes       | version of the prometheus stack chart                                                                                                                           |
| prometheus_stack_repo                         | yes       | chart of the prometheus stack                                                                                                                                   |
| monitoring_namespace                          |           | Name of the monitoring namespace                                                                                                                                |
| monitoring_ingress_grafana_tls                |           | If enabled, exposes Grafana through HTTPS on the ingress                                                                                                        |
| monitoring_grafana_ingress_dns                |           | The dns name used for exposing Grafana via ingress                                                                                                              |
| monitoring_prometheus_ingress_dns             |           | If enabled, exposes Prometheus through HTTPS on the ingress                                                                                                     |
| monitoring_prometheus_image_tag               |           | Prometheus container image tag, defaults to chart's default                                                                                                     |
| monitoring_prometheus_ingress_enabled         |           | Enables ingress for prometheus                                                                                                                                  |
| monitoring_prometheus_storage_spec            |           | Prometheus storage spec, see [Storage Configuration](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/storage.md) |
| monitoring_additional_ingress_annotations     |           | Annotations that will be attached to the ingress resource                                                                                                       |
| monitoring_grafana_admin_password             |           | Sets the admin password for Grafana                                                                                                                             |
| monitoring_grafana_dashboard_timezone         |           | Sets the default's dashboard timezone for Grafana                                                                                                               |
| monitoring_grafana_additional_datasources     |           | Configures additional datasources for Grafana                                                                                                                   |
| monitoring_grafana_github_oauth               |           | [Configure GitHub OAuth2 authentication](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/github/)             |
| monitoring_grafana_extra_secret_mounts        |           | Extra secret mounts                                                                                                                                             |
| monitoring_slack_channel_url                  |           | Slack channel url to add on alertmanager                                                                                                                        |
| monitoring_slack_channel                      |           | Slack channel to add on alertmanager                                                                                                                            |
| monitoring_metal_api_url                      |           | The URL where to reach metal-api                                                                                                                                |
| monitoring_metal_api_hmac                     |           | The hmac to authenticate against metal-api                                                                                                                      |
| monitoring_thanos_object_store_config         |           | Object storage used by Thanos, see [Official Documentation](https://thanos.io/tip/thanos/storage.md/#supported-clients)                                         |
| monitoring_thanos_receive_enabled             |           | Enable Thanos Receive component                                                                                                                                 |
| monitoring_thanos_receive_ingress_enabled     |           | Enable Ingress for Thanos Receive                                                                                                                               |
| monitoring_thanos_receive_ingress_annotations |           | Annotations that will be attached to the ingress resource for the Thanos Receive component                                                                      |
| monitoring_thanos_receive_ingress_basic_auth  |           | Set basic authentication on the Ingress for Thanos Receive                                                                                                      |
| monitoring_thanos_receive_ingress_dns         |           | The DNS name used for exposing Thanos Receive via Ingress                                                                                                       |
| monitoring_thanos_receive_ingress_tls         |           | If enabled, exposes Thanos Receive through HTTPS on the Ingress                                                                                                 |

### Gardener

| Name                                            | Mandatory | Description                                                 |
| ----------------------------------------------- | --------- | ----------------------------------------------------------- |
| monitoring_gardener_enabled                     |           | Enables monitoring for Gardener                             |
| monitoring_gardener_metrics_exporter_image_name |           | gardener-metrics-exporter image name                        |
| monitoring_gardener_metrics_exporter_image_tag  |           | gardener-metrics-exporter image tag                         |
| monitoring_gardener_virtual_garden_kubeconfig   |           | The kubeconfig for the kube-apiserver of the virtual garden |
