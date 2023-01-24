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
| monitoring_namespace                      |           | Name of the monitoring namespace                            |
| monitoring_prometheus_tag                 |           | Prometheus container image tag, defaults to chart's default |
| monitoring_alertlogger_image_name         | yes       | Alertlogger image name                                      |
| monitoring_alertlogger_image_tag          | yes       | Alertlogger image tag                                       |
| monitoring_eventrouter_image_name         | yes       | eventrouter image name                                      |
| monitoring_eventrouter_image_tag          | yes       | eventrouter image tag                                       |
| monitoring_additional_ingress_annotations |           | Annotations that will be attached to the ingress resource   |
| monitoring_ingress_dns                    |           | The dns name used for exposing services via ingress         |
| monitoring_ingress_grafana_tls            |           | Enables TLS for monitoring                                  |
| monitoring_prometheus_ingress_value       |           | Enables ingress for prometheus                              |

