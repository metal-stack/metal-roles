# gardener-managed-seeds

Deploys managed seeds into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                                       | Mandatory | Description                                                                                     |
| ------------------------------------------ | --------- | ----------------------------------------------------------------------------------------------- |
| gardener_managed_seeds_garden_name         |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden     |
| gardener_managed_seed_default_dns_provider |           | The dns provider used by this managed seed                                                      |
| gardener_managed_seed_default_dns_domain   |           | The dns domain used by this managed seed for ingress                                            |
| gardener_managed_seeds                     |           | The configuration for the managed seeds deployed into the Garden cluster                        |
| gardener_managed_seed_defaults             |           | Defaults configuration for the managed seeds (specific configuration overwrites these defaults) |
