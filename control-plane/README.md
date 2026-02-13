# control-plane

Contains roles for deploying the metal-control-plane.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)
- an ingress-controller in your cluster ([nginx-ingress](https://github.com/kubernetes/ingress-nginx) is the default of this project)
- As our control plane also requires layer-4 services to be exposed to the outside world, you need to take care of exposing them in order to make them reachable from a partition. This can for instance be achieved through [tcp and udp service exposal of Kubernetes nginx-ingress](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/). You can look up how it can be done in the [mini-lab](https://github.com/metal-stack/mini-lab). Here comes the list of required ports:

    | Port  | Protocol | Service Name  | Description                   |
    | ----- | -------- | ------------- | ----------------------------- |
    | 4150  | TCP      | nsqd          | nsq Daemon (TLS)              |
    | 5222  | TCP      | metal-console | Console forwarding (SSH)      |
    | 50051 | TCP      | metal-api     | metal-api gRPC API (protobuf) |

## Variables

The `defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all [the default values](roles/defaults/defaults/main.yaml).

| Name                                  | Mandatory | Description                                                                                         |
| ------------------------------------- | --------- | --------------------------------------------------------------------------------------------------- |
| metal_control_plane_provider_tenant   |           | The name of the provider tenant, has extended privileges                                            |
| metal_control_plane_ingress_dns       | yes       | The dns name used for exposing services via ingress                                                 |
| metal_control_plane_stage_name        |           | The name of the current stage, can be used for prefixing                                            |
| metal_control_plane_namespace         |           | The target namespace of all deployed kubernetes resources of the metal-control-plane                |
| metal_control_plane_image_pull_policy |           | Global value for an ImagePullPolicy that will be used for Kubernetes entities                       |
| metal_control_plane_host_provider     |           | The control-planes hosting provider, one of `metal` or `gcp`. Required for gardener deployment.     |

## Roles

| Role Name                                                              | Description                                                                                                                        |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [auditing-meili](roles/auditing-meili)                                 | Deploys an audit backend based on meilisearch                                                                                      |
| [auditing-timescaledb](roles/auditing-timescaledb)                     | Deploys an audit backend based on timescaledb                                                                                      |
| [gardener-cloud-profile](roles/gardener-cloud-profile)                 | Deploys a Gardener cloud profile for metal-stack                                                                                   |
| [gardener-extensions](roles/gardener-extensions)                       | Deploys Gardener operator extension resources                                                                                      |
| [gardener-gardenlet](roles/gardener-gardenlet)                         | Deploys Gardener operator gardenlet resources                                                                                      |
| [gardener-managed-seeds](roles/gardener-managed-seeds)                 | Deploys managed seeds into the virtual garden                                                                                      |
| [gardener-monitoring-certs](roles/gardener-monitoring-certs)           | Deploys monitoring ingress certificates for seed clusters                                                                          |
| [gardener-operator](roles/gardener-operator)                           | Deploys the Gardener operator                                                                                                      |
| [gardener-partition-proxy](roles/gardener-partition-proxy)             | Deploys a partition proxy into a shooted seed                                                                                      |
| [gardener-projects](roles/gardener-projects)                           | Deploys gardener projects into the virtual garden.                                                                                 |
| [gardener-shoots](roles/gardener-shoots)                               | Deploys managed shoots into the virtual garden.                                                                                    |
| [gardener-virtual-garden-access](roles/gardener-virtual-garden-access) | Deploys a managed resource to access the the Virtual Garden with operator setup                                                    |
| [headscale](roles/headscale)                                           | Deploys headscale for firewall VPN                                                                                                 |
| [ipam-db](roles/ipam-db)                                               | Deploys a database for the [IPAM](https://github.com/metal-stack/go-ipam) of the metal-api                                         |
| [isolated-clusters](roles/isolated-clusters)                           | Deploys services for Gardener isolated clusters                                                                                    |
| [logging](roles/logging)                                               | Deploys metal-stack control plane logging components                                                                               |
| [masterdata-db](roles/masterdata-db)                                   | Deploys a database for the masterdata-api                                                                                          |
| [meili-backup-restore](roles/meili-backup-restore)                     | A role for deploying a meilisearch database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar) |
| [metal-db](roles/metal-db)                                             | Deploys a database for the metal-api                                                                                               |
| [metal-python](roles/metal-python)                                     | Installs metal-python                                                                                                              |
| [metal](roles/metal)                                                   | Deploys all metal-stack components of the metal-control-plane via Helm chart                                                       |
| [monitoring](roles/monitoring)                                         | Deploys metal-stack control plane monitoring components                                                                            |
| [nsq](roles/nsq)                                                       | Deploys [nsq](https://nsq.io/)                                                                                                     |
| [postgres-backup-restore](roles/postgres-backup-restore)               | A role for deploying a postgres database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar)    |
| [prepare](roles/prepare)                                               | Contains tasks for preparing the deployment of the metal-control-plane                                                             |
| [rethinkdb-backup-restore](roles/rethinkdb-backup-restore)             | A role for deploying a rethinkdb database with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar)   |
| [valkey](roles/valkey)                                                 | Deploys a valkey cluster                                                                                                           |

## Examples

An example playbook for deploying the metal-control-plane with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
