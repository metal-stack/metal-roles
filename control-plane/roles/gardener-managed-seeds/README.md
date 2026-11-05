# gardener-managed-seeds

Deploys managed seeds into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# REQUIRED: The default DNS domain used for the internal seed DNS entries.
gardener_managed_seed_default_dns_domain: null
# The default DNS provider used for the seed DNS entries.
gardener_managed_seed_default_dns_provider: null
# Default configuration merged into every managed seed entry.
gardener_managed_seed_defaults:
  excess_capacity_reservation: true
  external_traffic_policy: Local
  visible: true
# The managed seeds to deploy.
gardener_managed_seeds: []
# Name of the garden to deploy the managed seeds to.
gardener_managed_seeds_garden_name: '{{ gardener_defaults_garden_name }}'
```
