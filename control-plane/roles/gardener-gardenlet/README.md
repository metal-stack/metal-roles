# gardener-gardenlet

Deploys an operator Gardenlet resource into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# REQUIRED: The credentials for the default DNS provider.
gardener_gardenlet_default_dns_credentials: null
# REQUIRED: The default DNS domain used for the seed DNS entries.
gardener_gardenlet_default_dns_domain: null
# REQUIRED: The default DNS provider used for the seed DNS entries.
gardener_gardenlet_default_dns_provider: null
# Default configuration merged into every gardenlet entry.
gardener_gardenlet_defaults:
  backup_entry_deletion_grace_period_hours: 72
  component_image_vector_overwrite: []
  feature_gates: {}
  garden_client_connection: null
  image_vector_overwrite: []
  kubeconfigSecretRef: null
  logging_enabled: false
  logging_vali_enabled: false
  logging_vali_storage: 100Gi
  shoot_concurrent_syncs: 20
  shoot_reconcile_in_maintenance_only: true
  shoot_respect_sync_period_overwrite: true
  vertical_pod_autoscaler_enabled: true
# Name of the garden to deploy the gardenlets to.
gardener_gardenlet_garden_name: '{{ gardener_defaults_garden_name }}'
# Tag of the gardenlet helm chart. Derived from the gardenlet image tag of the release vector by default.
gardener_gardenlet_helm_chart_tag: '{{ gardener_gardenlet_image_tag }}'
# The gardenlets to deploy.
gardener_gardenlets: []
```
