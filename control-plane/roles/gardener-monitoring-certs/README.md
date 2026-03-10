# gardener-monitoring-certs

Deploys a control plane certificate to the soil and the seeds in order to provide monitoring certificates for the Grafanas. This role can only be executed when seed api servers are reachable.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Requirements

- Requires cert-manager with DNS cluster issuer to be deployed in the Garden cluster

## Variables

| Name                                                 | Mandatory | Description                                                                                                      |
| ---------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| gardener_monitoring_certs_garden_name                | yes       | The name of operator garden resource to derive the access kubeconfig for the virtual garden                      |
| gardener_monitoring_certs_certificate_cluster_issuer | yes       | The issuer used for deploying a certificate for the Gardener monitoring ingresses for TLS                        |
| gardener_monitoring_certs_ingress_domain             | yes       | The base domain used by the ingress on which a wildcard certificate will be issued for the monitoring components |
| gardener_monitoring_certs_shooted_seeds              |           | A list of shooted seeds on which to provide the monitoring cert                                                  |
