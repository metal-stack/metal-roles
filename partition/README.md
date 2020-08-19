# partition

Contains roles for deploying the metal-partition.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)

## Variables

The `partition-defaults` folder contains defaults that are used by multiple roles in the partition directory.

You can look up all the default values [here](partition-defaults/main.yaml).

| Name                                    | Mandatory | Description                                                                                      |
| --------------------------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| metal_partition_id                      | yes       | The id of this partition. This needs to correspond to the partition id defined in the metal-api. |
| metal_partition_mgmt_gateway            | yes       |                                                                                                  |
| metal_partition_timezone                | yes       | The timezone in which this partition is located                                                  |
| metal_partition_metal_api_addr          | yes       | The address of the metal-api that this partition connects to                                     |
| metal_partition_metal_api_port          |           | The port of the metal-api that this partition connects to                                        |
| metal_partition_metal_api_grpc_port     |           | The port of the metal-api gRPC server that this partition connects to                            |
| metal_partition_metal_api_protocol      |           | The protocol of the metal-api that this partition connects to                                    |
| metal_partition_metal_api_basepath      |           | The basepath of the metal-api that this partition connects to                                    |
| metal_partition_metal_api_hmac_edit_key |           | The HMAC edit key used for authenticating at the metal-api                                       |

## Roles

| Role Name                                    | Description                                     |
| -------------------------------------------- | ----------------------------------------------- |
| [bmc-proxy](roles/bmc-proxy)                 | Deploys a bmc-proxy                             | 
| [dhcp](roles/dhcp)                           | Deploys a dhcp server                           |
| [docker-on-cumulus](roles/docker-on-cumulus) | Deploys docker on cumulus                       |
| [ipmi-catcher](roles/ipmi-catcher)           | Deploys ipmi-catcher to crawl ipmi ip addresses |
| [leaf](roles/leaf)                           | Deploys network config for cumulus switches     |
| [metal-core](roles/metal-core)               | Deploys metal-core                              |
| [pixiecore](roles/pixiecore)                 | Deploys pixiecore                               |
| [router](roles/router)                       | Deploys router config on cumulus switches       |

## Examples

An example playbook for deploying the metal-partition with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
