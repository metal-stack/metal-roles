# gardener-logging

This role deploys a promtail into a Gardener shooted seed. It is expected that the [logging role](../logging/) was deployed into the metal-stack control plane before executing this role.

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

The following variables can be set to configure the role:

### General

| Name                                              | Mandatory | Description                                                      |
| ------------------------------------------------- | --------- | ---------------------------------------------------------------- |
| gardener_logging_promtail_chart_version           | yes       | Helm chart version for promtail specified under release vector   |
| gardener_logging_promtail_chart_repo              | yes       | Repository for promtail specified under release vector           |
| gardener_logging_namespace                        |           | The deployment's target namespace                                |
| gardener_logging_ingress_dns                      |           | DNS for loki ingress                                             |
| gardener_logging_ingress_loki_basic_auth_password |           | The basic auth password for the external loki ingress            |
| gardener_logging_ingress_loki_basic_auth_user     |           | The basic auth user for the external loki ingress                |
| gardener_logging_deploy_to_garden_cluster         |           | Deploys promtail also into the garden cluster                    |
| gardener_logging_shooted_seeds                    |           | Shooted seed names on which to deploy promtails that log to loki |
