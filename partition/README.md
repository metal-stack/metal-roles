# partition

Contains roles for deploying the metal-partition.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)

## Variables

The `partition-defaults` folder contains defaults that are used by multiple roles in the partition directory.

You can look up all the default values [here](partition-defaults/main.yaml).

| Name                                | Mandatory | Description                                                                                                              |
| ----------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| partition_nameservers               | yes       | A list of nameservers                                                                                                    |
| partition_id                        | yes       | Partition id                                                                                                             |


## Roles

| Role Name                                                                | Description                                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [dhcp](roles/dhcp)                                                       | Deploys a dhcp server                                                                                                           |
| [docker-on-cumulus](roles/docker-on-cumulus)                             | Deploys docker on cumulus                                                                                                       |
| [ipmi-catcher](roles/ipmi-catcher)                                       | Deploys ipmi-catcher to crawl ipmi ip addresses                                                                                 |
| [leaf](roles/leaf)                                                       | Deploys network config for cumulus switches                                                                                     |
| [pixiecore](roles/pixiecore)                                             | Deploys pixiecore                                                                                                               |
| [router](roles/router)                                                   | Deploys router config on cumulus switches                                                                                       |

## Examples

An example playbook for deploying the metal-partition with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
