# control-plane

Contains roles for deploying the metal-control-plane.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)
- an ingress-controller in your cluster ([nginx-ingress](https://github.com/kubernetes/ingress-nginx) is the default of this project, you need to parametrize the roles carefully if you want to use another ingress-controller. when you just use nginx-ingress, make sure to also deploy it to the default namespace `ingress-nginx`)

## Variables

The `global-defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all the default values [here](../global-defaults/main.yaml).

| Name                               | Mandatory | Description                                                                                                                                                |
| ---------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| metal_stack_release_version        |           | If defined fetches image versions from the [release](https://github.com/metal-stack/releases) vector, such that image names and tags are getting populated |
| metal_stack_release_vector_mapping |           | Describes the paths to map images from the release vector to the roles in this repository                                                                  |

The `control-plane-defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all the default values [here](control-plane-defaults/main.yaml).

| Name                                | Mandatory | Description                                                                                                              |
| ----------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| metal_control_plane_provider_tenant |           | The name of the provider tenant, has extended privileges                                                                 |
| metal_control_plane_ingress_dns     | yes       | The dns name used for exposing services via ingress                                                                      |
| metal_control_plane_stage_name      |           | The name of the current stage, can be used for prefixing                                                                 |
| metal_control_plane_namespace       |           | The target namespace of all deployed kubernetes resources of the metal-control-plane                                     |
| metal_control_plane_host_provider   |           | The name of the provider where the control plane is hosted, can be used for provider specific switches in the automation |

## Roles

| Role Name                                                                | Description                                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [ipam-db](roles/ipam-db)                                   | Deploys a database for the [IPAM](https://github.com/metal-stack/go-ipam) of the metal-api                                      |
| [masterdata-db](roles/masterdata-db)                       | Deploys a database for the masterdata-api                                                                                       |
| [metal](roles/metal)                                       | Deploys all metal-stack components of the metal-control-plane via Helm                                                          |
| [metal-db](roles/metal-db)                                 | Deploys a database for the metal-api                                                                                            |
| [nsq](roles/nsq)                                           | Deploys [nsq](https://nsq.io/)                                                                                                  |
| [postgres-backup-restore](roles/postgres-backup-restore)   | A role for deploying a postgres database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar) |
| [prepare](roles/prepare)                                   | Contains tasks for preparing the deployment of the metal-control-plane                                                          |
| [rethinkdb-backup-restore](roles/rethinkdb-backup-restore) | A role for deploying a rethinkdb with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar)         |

## Examples

An example playbook for deploying the metal-control-plane with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
