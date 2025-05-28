# logging

This role is designed to set up logging using Ansible.
The role includes tasks to install and configure the following logging tools:

- Loki
- Logging ingress for Loki
- Promtail for monitoring the control plane cluster
- Promtail for monitoring Gardener seed clusters

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).
The following variables can be set to configure the role:

### General

| Name                                          | Mandatory | Description                                                    |
| --------------------------------------------- | --------- | -------------------------------------------------------------- |
| logging_chart_version                         | yes       | Helm chart version for loki specified under release vector     |
| logging_chart_repo                            | yes       | Repository for loki specified under release vector             |
| logging_promtail_chart_version                | yes       | Helm chart version for promtail specified under release vector |
| logging_promtail_chart_repo                   | yes       | Repository for promtail specified under release vector         |
| logging_namespace                             |           | The deployment's target namespace                              |
| logging_loki_size                             |           | The size of the volume that loki will use for storing logs     |
| logging_ingress_dns                           |           | DNS for loki ingress                                           |
| logging_ingress_loki_tls                      |           | If enabled, exposes loki through HTTPS on the ingress          |
| logging_ingress_loki_basic_auth_password_salt |           | The basic auth password salt used for stable password hashes   |
| logging_ingress_loki_basic_auth_password      |           | The basic auth password for the external loki ingress          |
| logging_ingress_loki_basic_auth_user          |           | The basic auth user for the external loki ingress              |

### Gardener

| Name                                       | Mandatory | Description                                                 |
| ------------------------------------------ | --------- | ----------------------------------------------------------- |
| logging_gardener_enabled                   |           | Enables logging for Gardener                                |
| logging_gardener_seeds                     |           | Seed names on which to deploy promtails that log to loki    |
| logging_gardener_virtual_garden_kubeconfig |           | The kubeconfig for the kube-apiserver of the virtual garden |
