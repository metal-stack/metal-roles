# gardener-shoots

Deploys shoots into the virtual garden. This can also be used for shooted seeds.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# The default metal-api HMAC used for the shoot infrastructure secrets.
gardener_shoot_default_metal_api_hmac: null
# Default configuration merged into every shoot entry.
gardener_shoot_defaults:
  additional_annotations: {}
  additional_labels: {}
  auto_update:
    kubernetes: true
    machine_image: false
  maintenance_timewindow_begin: 220000+0100
  maintenance_timewindow_end: 230000+0100
  max_pods: 250
  namespace: garden
  node_cidr_mask_size: 23
  tenant: '{{ metal_control_plane_provider_tenant }}'
  vertical_pod_autoscaler: true
# Delay in seconds between retries when waiting for shoot reconciliation.
gardener_shoot_rollout_wait_delay: 10
# Whether to wait for shoot reconciliation to succeed.
gardener_shoot_rollout_wait_enabled: true
# Amount of retries when waiting for shoot reconciliation.
gardener_shoot_rollout_wait_retries: 36
# The shoot clusters to deploy.
gardener_shoots: []
# Name of the garden to deploy the shoots to.
gardener_shoots_garden_name: '{{ gardener_defaults_garden_name }}'
```
