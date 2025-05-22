# gardener-gardenlet

Deploys an operator Gardenlet resource into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                                       | Mandatory | Description                                                                                 |
| ------------------------------------------ | --------- | ------------------------------------------------------------------------------------------- |
| gardener_gardenlet_garden_name             |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden |
| gardener_gardenlet_helm_chart              |           | The ref to the helm oci artifact to deploy the gardenlet                                    |
| gardener_gardenlet_helm_chart_tag          |           | The tag of the helm oci artifact to deploy the gardenlet                                    |
| gardener_gardenlet_image_name              |           | The gardenlet container image name                                                          |
| gardener_gardenlet_image_tag               |           | The gardenlet container image tag                                                           |
| gardener_gardenlet_default_dns_domain      | true      | The dns of the default domain (and internal domain)                                         |
| gardener_gardenlet_default_dns_provider    | true      | The dns provider of the default domain (and internal domain)                                |
| gardener_gardenlet_default_dns_credentials | true      | The dns provider credentials of the default domain (and internal domain)                    |
| gardener_gardenlet_local                   |           | The configuration for a Gardenlet deployed into the Garden cluster                          |
