# gardener-shoots

Deploys shoots into the virtual garden. This can also be used for shooted seeds.

Please refer to the metal-stack gardener integration in
our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                          | Mandatory | Description                                                                                 |
| ----------------------------- | --------- | ------------------------------------------------------------------------------------------- |
| gardener_projects_garden_name |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden |
| gardener_projects             |           | The configuration for the projects deployed into the Garden cluster                         |
| gardener_project_defaults     |           | Defaults configuration for the projects (specific configuration overwrites these defaults)  |
