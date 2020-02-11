# control-plane

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)

## Variables

The `control-plane-defaults` folder contains defaults that are used by multiple roles in the control-plane directory.

You can look up all the default values [here](control-plane-defaults/main.yaml).

| Name                                | Mandatory | Description                                                |
| ----------------------------------- | --------- | ---------------------------------------------------------- |
| metal_control_plane_provider_tenant | yes       | The name of the provider tenant, has extended privileges   |
| metal_control_plane_ingress_dns     | yes       | The dns name used for exposing services via ingress        |
| metal_control_plane_stage_name      |           | The name of the current stage, can be used for prefixing   |
| metal_control_plane_namespace       |           | The target namespace of all deployed kubernetes resources  |
| metal_control_plane_host_provider   |           | The name of the provider where the control plane is hosted |

## Roles

| Role Name                                                                | Description                                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [ipam-db](control-plane/roles/ipam-db)                                   | Deploys a database for the [IPAM](https://github.com/metal-stack/go-ipam) of the metal-api                                      |
| [masterdata-db](control-plane/roles/masterdata-db)                       | Deploys a database for the masterdata-api                                                                                       |
| [metal](control-plane/roles/metal)                                       | Deploys all Metal Stack components of the metal-control-plane via Helm                                                          |
| [metal-db](control-plane/roles/metal-db)                                 | Deploys a database for the metal-api                                                                                            |
| [nsq](control-plane/roles/nsq)                                           | Deploys [nsq](https://nsq.io/)                                                                                                  |
| [postgres-backup-restore](control-plane/roles/postgres-backup-restore)   | A role for deploying a postgres database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar) |
| [prepare](control-plane/roles/prepare)                                   | Contains tasks for preparing the deployment of the metal-control-plane                                                          |
| [rethinkdb-backup-restore](control-plane/roles/rethinkdb-backup-restore) | A role for deploying a rethinkdb with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar)         |

## Examples

An example playbook for deploying the metal-control-plane with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
