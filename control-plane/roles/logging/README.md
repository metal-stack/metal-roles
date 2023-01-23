# logging

This role is designed to set up logging using Ansible.
The role includes tasks to install and configure the following logging tools:

- Loki-stack
- Logging ingress for Loki

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).
The following variables can be set to configure the role:

### General

| Name                     | Mandatory | Description                                                |
| ------------------------ | --------- | ---------------------------------------------------------- |
| logging_chart_version    | yes       | Helm chart version specified under release vector          |
| logging_chart_repo       | yes       | Repository specified under release vector                  |
| logging_namespace        |           | The deployment's target namespace                          |
| logging_ingress_dns      |           | DNS for loki ingress                                       |
| logging_ingress_loki_tls |           | If enabled, exposes loki with a TLS secret doing mTLS      |
| logging_loki_size        |           | The size of the volume that loki will use for storing logs |
