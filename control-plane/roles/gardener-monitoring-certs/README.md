# gardener-monitoring-certs

Deploys a control plane certificate to the soil and the seeds in order to provide monitoring certificates for the Grafanas. This role can only be executed when seed api servers are reachable.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role mainly tries to inherit variables from the `gardener` role, so it does not require many own variables.

| Name                                      | Mandatory | Description                                                                               |
| ----------------------------------------- | --------- | ----------------------------------------------------------------------------------------- |
| gardener_seeds_certificate_cluster_issuer | yes       | The issuer used for deploying a certificate for the Gardener monitoring ingresses for TLS |
| gardener_seeds_dns_domain                 |           | The DNS domain used by the seeds                                                          |
| gardener_seeds_shooted_seeds              |           | A list of definitions for shooted seeds                                                   |
| gardener_seeds_soil_name                  |           | The name of the initial `Seed` (used for spinning up shooted seeds)                       |
| gardener_seeds_virtual_garden_kubeconfig  |           | The kubeconfig for the kube-apiserver of the virtual garden                               |
