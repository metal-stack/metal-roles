# gardener-monitoring-certs

Deploys a control plane certificate to the soil and the seeds in order to provide monitoring certificates for the Grafanas. This role can only be executed when seed api servers are reachable.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Requirements

- Requires cert-manager with DNS cluster issuer to be deployed in the Garden cluster

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Name of the cert-manager ClusterIssuer used for issuing the seed ingress certificate.
gardener_monitoring_certs_certificate_cluster_issuer: null
# Name of the garden.
gardener_monitoring_certs_garden_name: '{{ gardener_defaults_garden_name }}'
# The ingress domain for which the wildcard certificate is issued.
gardener_monitoring_certs_ingress_domain: null
# The shooted seeds (name, ingress_domain) to distribute the certificates to.
gardener_monitoring_certs_shooted_seeds: []
```
