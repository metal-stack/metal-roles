# gardener-projects

Deploys projects into the virtual garden.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Default configuration merged into every project entry.
gardener_project_defaults:
  additional_labels: {}
  members: []
  namespace: garden
  owner: admin
  protected_toleration: true
# The Gardener projects to deploy (name, description, members, protected_toleration).
gardener_projects: []
# Name of the garden to deploy the projects to.
gardener_projects_garden_name: '{{ gardener_defaults_garden_name }}'
```
