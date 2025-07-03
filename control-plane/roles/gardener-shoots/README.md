# gardener-shoots

Deploys shoots into the virtual garden. This can also be used for shooted seeds.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                                  | Mandatory | Description                                                                                 |
| ------------------------------------- | --------- | ------------------------------------------------------------------------------------------- |
| gardener_shoots_garden_name           |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden |
| gardener_shoot_default_metal_api_hmac |           | For the cloud provider credentials                                                          |
| gardener_shoots                       |           | The configuration for the shoots deployed into the Garden cluster                           |
| gardener_shoot_defaults               |           | Defaults configuration for the shoots (specific configuration overwrites these defaults)    |
| gardener_shoot_rollout_wait_enabled   |           | If enabled waits until the shoot was successfully reconciled                                |
| gardener_shoot_rollout_wait_retries   |           | The maximum amount of retries until giving up                                               |
| gardener_shoot_rollout_wait_delay     |           | The delay between the retries                                                               |
