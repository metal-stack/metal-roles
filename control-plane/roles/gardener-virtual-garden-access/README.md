# gardener-virtual-garden-access

Creates a managed resource that rotates the token for a valid kubeconfig to access the Virtual Garden as described in <https://gardener.cloud/docs/gardener/concepts/operator/#virtual-garden-kubeconfig>.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Cluster role bindings deployed to the virtual garden.
gardener_virtual_garden_access_cluster_role_bindings: []
# Token expiration duration for the virtual garden access service account.
gardener_virtual_garden_access_expiration: 8h
# Name of the garden to create the access resources for.
gardener_virtual_garden_access_garden_name: '{{ gardener_defaults_garden_name }}'
```
