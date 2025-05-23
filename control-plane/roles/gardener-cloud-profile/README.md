# gardener-cloud-profile

Deploys a Gardener Cloud Profile for metal-stack into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                                                       | Mandatory | Description                                                                                                                     |
| ---------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| gardener_cloud_profile_garden_name                         |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden                                     |
| gardener_cloud_profile_wait_until_available                |           | If set to true, waits for the cloud profile resource to be registered in the virtual garden (helpful for initial bootstrapping) |
| gardener_cloud_profile_stage_name                          |           | The name of the metal control plane in the cloud profile                                                                        |
| gardener_cloud_profile_metal_api_url                       |           | The URL used by the Gardener to communicate with the metal-api                                                                  |
| gardener_cloud_profile_machine_images                      |           | The machine images available for shoots in the metal-api                                                                        |
| gardener_cloud_profile_firewall_images                     |           | The firewall images available for shoots in the metal-api                                                                       |
| gardener_cloud_profile_firewall_images_from_machine_images |           | If set to true, uses the passed machine images and adds those with firewall feature                                             |
| gardener_cloud_profile_firewall_controller_versions        |           | The available firewall controller versions for metal-stack shoots                                                               |
| gardener_cloud_profile_kubernetes                          | yes       | The available Kubernetes versions for metal-stack shoots                                                                        |
| gardener_cloud_profile_machine_types                       |           | The machine types available for shoots in the metal-api                                                                         |
| gardener_cloud_profile_regions                             | yes       | The regions available for shoots                                                                                                |
| gardener_cloud_profile_partitions                          |           | The partitions available for shoots                                                                                             |
| gardener_cloud_profile_os_cri_mapping                      |           | A mapping to add available CRIs to the machine images                                                                           |
| gardener_cloud_profile_os_compatibility_mapping            |           | A mapping to add kubelet version constraints to the machine images                                                              |
