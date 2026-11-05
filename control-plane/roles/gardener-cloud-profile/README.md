# gardener-cloud-profile

Deploys a Gardener Cloud Profile for metal-stack into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Firewall controller versions offered in the cloud profile.
gardener_cloud_profile_firewall_controller_versions: []
# Firewall images offered in the cloud profile.
gardener_cloud_profile_firewall_images: []
# Whether firewall images are derived from the machine images.
gardener_cloud_profile_firewall_images_from_machine_images: true
# Name of the garden to deploy the cloud profile to.
gardener_cloud_profile_garden_name: '{{ gardener_defaults_garden_name }}'
# REQUIRED: The kubernetes section (expirable versions) of the cloud profile. Mandatory, must not be none.
gardener_cloud_profile_kubernetes: null
# Machine images offered in the cloud profile. Defaults to metal_api_images.
gardener_cloud_profile_machine_images: '{{ metal_api_images | default([]) }}'
# Machine types offered in the cloud profile.
gardener_cloud_profile_machine_types: []
# The metal-api URL rendered into the cloud profile.
gardener_cloud_profile_metal_api_url: https://api.{{ metal_control_plane_gateway_dns }}
# Mapping of operating systems to kubelet compatibility constraints.
gardener_cloud_profile_os_compatibility_mapping: {}
# Mapping of operating systems to supported container runtimes.
gardener_cloud_profile_os_cri_mapping:
  debian:
    cris:
    - containerRuntimes: []
      name: containerd
    when: null
  ubuntu:
    cris:
    - containerRuntimes: []
      name: containerd
    when: null
# Per-partition configuration (e.g. default machine types) of the cloud profile.
gardener_cloud_profile_partitions: {}
# REQUIRED: The regions section of the cloud profile. Mandatory, must not be none.
gardener_cloud_profile_regions: null
# The stage name rendered into the cloud profile.
gardener_cloud_profile_stage_name: '{{ metal_control_plane_stage_name }}'
# Whether to wait until the CloudProfile resource is available in the virtual garden.
gardener_cloud_profile_wait_until_available: true
```
