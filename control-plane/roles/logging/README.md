# logging

This role is designed to set up logging using Ansible.
The role includes tasks to install and configure the following logging tools:

- Loki
- Logging ingress for Loki

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).
The following variables can be set to configure the role:

### General

| Name                           | Mandatory | Description                                                    |
| ------------------------------ | --------- | -------------------------------------------------------------- |
| logging_chart_version          | yes       | Helm chart version for loki specified under release vector     |
| logging_chart_repo             | yes       | Repository for loki specified under release vector             |
| logging_promtail_chart_version | yes       | Helm chart version for promtail specified under release vector |
| logging_promtail_chart_repo    | yes       | Repository for promtail specified under release vector         |
| logging_namespace              |           | The deployment's target namespace                              |
| logging_ingress_dns            |           | DNS for loki ingress                                           |
| logging_ingress_loki_tls       |           | If enabled, exposes loki through HTTPS on the ingress          |
| logging_loki_size              |           | The size of the volume that loki will use for storing logs     |
