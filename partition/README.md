# partition

Contains roles for deploying the metal-partition.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)

## Variables

The `partition-defaults` folder contains defaults that are used by multiple roles in the partition directory.

You can look up all the default values [here](partition-defaults/main.yaml).

| Name                                                | Mandatory | Description                                                                                      |
| --------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| metal_partition_id                                  | yes       | The id of this partition. This needs to correspond to the partition id defined in the metal-api. |
| metal_partition_mgmt_gateway                        | yes       |                                                                                                  |
| metal_partition_timezone                            | yes       | The timezone in which this partition is located                                                  |
| metal_partition_metal_api_addr                      | yes       | The address of the metal-api that this partition connects to                                     |
| metal_partition_metal_api_port                      |           | The port of the metal-api that this partition connects to                                        |
| metal_partition_metal_api_protocol                  |           | The protocol of the metal-api that this partition connects to                                    |
| metal_partition_metal_api_basepath                  |           | The basepath of the metal-api that this partition connects to                                    |
| metal_partition_metal_api_hmac_edit_key             | yes       | The HMAC edit key used for authenticating at the metal-api                                       |
| metal_partition_metal_api_hmac_view_key             | yes       | The HMAC view key used for authenticating at the metal-api                                       |
| metal_partition_metal_api_grpc_address              |           | The address of metal-api grpc endpoint in the form (ip or hostname:port)                         |
| metal_partition_metal_api_grpc_cert_dir             |           | The directory where the grpc certificates reside                                                 |
| metal_partition_metal_api_grpc_ca_cert              | yes       | The ca certificate file content                                                                  |
| metal_partition_metal_api_grpc_client_cert          | yes       | The client certificate file content                                                              |
| metal_partition_metal_api_grpc_client_key           | yes       | The client certificate key file content                                                          |
| metal_partition_metal_core_additional_volume_mounts |           |

## Roles

| Role Name                                    | Description               |
| -------------------------------------------- | ------------------------- |
| [bmc-proxy](roles/bmc-proxy)                 | Deploys a bmc-proxy       |
| [dhcp](roles/dhcp)                           | Deploys a dhcp server     |
| [dhcp-relay](roles/dhcp-relay)               | Deploys a dhcp-relay      |
| [docker-on-cumulus](roles/docker-on-cumulus) | Deploys docker on cumulus |
| [metal-bmc](roles/metal-bmc)                 | Deploys metal-bmc         |
| [metal-core](roles/metal-core)               | Deploys metal-core        |
| [pixiecore](roles/pixiecore)                 | Deploys pixiecore         |
| [promtail](roles/promtail)                   | Deploys promtail          |

## Examples

An example playbook for deploying the metal-partition with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
