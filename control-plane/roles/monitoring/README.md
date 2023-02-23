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

| Name                                      | Mandatory | Description                                                 |
| ----------------------------------------- | --------- | ----------------------------------------------------------- |
| rethinkdb_exporter_name                   | yes       | rethinkdb exporter image name                               |
| rethinkdb_exporter_tag                    | yes       | rethinkdb exporter image tag                                |
| event_exporter_name                       | yes       | event exporter image name                                   |
| event_exporter_tag                        | yes       | event exporter image tag                                    |
| prometheus_chart_version                  | yes       | version of the prometheus stack chart                       |
| prometheus_stack_repo                     | yes       | chart of the prometheus stack                               |
| monitoring_namespace                      |           | Name of the monitoring namespace                            |
| monitoring_ingress_grafana_tls            |           | If enabled, exposes Grafana through HTTPS on the ingress    |
| monitoring_grafana_ingress_dns            |           | The dns name used for exposing Grafana via ingress          |
| monitoring_prometheus_ingress_dns         |           | If enabled, exposes Prometheus through HTTPS on the ingress |
| monitoring_prometheus_image_tag           |           | Prometheus container image tag, defaults to chart's default |
| monitoring_prometheus_ingress_enabled     |           | Enables ingress for prometheus                              |
| monitoring_additional_ingress_annotations |           | Annotations that will be attached to the ingress resource   |
| monitoring_grafana_admin_password         |           | Sets the admin password for Grafana                         |
| monitoring_grafana_dashboard_timezone     |           | Sets the default's dashboard timezone for Grafana           |
| monitoring_grafana_additional_datasources |           | Configures additional datasources for Grafana               |
| monitoring_metal_api_url                  |           | The URL where to reach metal-api                            |
| monitoring_metal_api_hmac                 |           | The hmac to authenticate against metal-api                  |
