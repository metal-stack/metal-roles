# gardener-virtual-garden-access

Creates a managed resource that rotates the token for a valid kubeconfig to access the Virtual Garden as described in <https://gardener.cloud/docs/gardener/concepts/operator/#virtual-garden-kubeconfig>.

## Variables

| Name                                       | Mandatory | Description                                                                                 |
| ------------------------------------------ | --------- | ------------------------------------------------------------------------------------------- |
| gardener_virtual_garden_access_garden_name |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden |
| gardener_virtual_garden_access_expiration  |           | The duration how long the token is valid for the access kubeconfig until it expires         |
