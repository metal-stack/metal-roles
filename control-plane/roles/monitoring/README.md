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
| logging_chart_version                     | yes       | version of the logging stack chart                          |
| logging_chart_repo                        | yes       | chart of the logging stack                                  |
| prometheus_chart_version                  | yes       | version of the prometheus stack chart                       |
| prometheus_stack_repo                     | yes       | chart of the prometheus stack                               |
| monitoring_namespace                      |           | Name of the monitoring namespace                            |
| monitoring_prometheus_tag                 |           | Prometheus container image tag, defaults to chart's default |
| monitoring_additional_ingress_annotations |           | Annotations that will be attached to the ingress resource   |
| monitoring_ingress_dns                    |           | The dns name used for exposing services via ingress         |
| monitoring_ingress_grafana_tls            |           | Enables TLS for monitoring                                  |
| monitoring_prometheus_ingress_enabled     |           | Enables ingress for prometheus                              |
