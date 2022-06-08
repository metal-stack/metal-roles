# control-plane

Contains roles for deploying the metal-control-plane.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)
- an ingress-controller in your cluster ([nginx-ingress](https://github.com/kubernetes/ingress-nginx) is the default of this project)
- As our control plane also requires layer-4 services to be exposed to the outside world, you need to take care of exposing them in order to make them reachable from a partition. This can for instance be achieved through [tcp and udp service exposal of Kubernetes nginx-ingress](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/). You can look up how it can be done in the [mini-lab](https://github.com/metal-stack/mini-lab). Here comes the list of required ports:

    | Port  | Protocol | Service Name  | Description                   |
    | ----- | -------- | ------------- | ----------------------------- |
    | 4150  | TCP      | nsqd          | nsq Daemon (HTTPS)            |
    | 4161  | TCP      | nsq-lookupd   | nsqlookup Damon (HTTP)        |
    | 5222  | TCP      | metal-console | Console forwarding (SSH)      |
    | 50051 | TCP      | metal-api     | metal-api gRPC API (protobuf) |

## Variables

The `control-plane-defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all the default values [here](control-plane-defaults/main.yaml).

| Name                                  | Mandatory | Description                                                                                                              |
| ------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| metal_control_plane_provider_tenant   |           | The name of the provider tenant, has extended privileges                                                                 |
| metal_control_plane_ingress_dns       | yes       | The dns name used for exposing services via ingress                                                                      |
| metal_control_plane_stage_name        |           | The name of the current stage, can be used for prefixing                                                                 |
| metal_control_plane_namespace         |           | The target namespace of all deployed kubernetes resources of the metal-control-plane                                     |
| metal_control_plane_image_pull_policy |           | Global value for an ImagePullPolicy that will be used for Kubernetes entities                                            |

## Roles

| Role Name                                                  | Description                                                                                                                     |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [headscale](roles/headscale)                               | Deploys headscale                                                                                                               |
| [ipam-db](roles/ipam-db)                                   | Deploys a database for the [IPAM](https://github.com/metal-stack/go-ipam) of the metal-api                                      |
| [masterdata-db](roles/masterdata-db)                       | Deploys a database for the masterdata-api                                                                                       |
| [metal](roles/metal)                                       | Deploys all metal-stack components of the metal-control-plane via Helm                                                          |
| [metal-db](roles/metal-db)                                 | Deploys a database for the metal-api                                                                                            |
| [metal-python](roles/metal-python)                         | Installs metal-python                                                                                                           |
| [nsq](roles/nsq)                                           | Deploys [nsq](https://nsq.io/)                                                                                                  |
| [postgres-backup-restore](roles/postgres-backup-restore)   | A role for deploying a postgres database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar) |
| [prepare](roles/prepare)                                   | Contains tasks for preparing the deployment of the metal-control-plane                                                          |
| [rethinkdb-backup-restore](roles/rethinkdb-backup-restore) | A role for deploying a rethinkdb with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar)         |

## Examples

An example playbook for deploying the metal-control-plane with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
