# partition

Contains roles for deploying the metal-partition.

## Requirements

- [ansible-common](https://github.com/metal-stack/ansible-common)

## Variables

The `parition-defaults` folder contains defaults that are used by multiple roles in the control-plane directory.

You can look up all the default values [here](partition-defaults/main.yaml).

| Name                                | Mandatory | Description                                                                                                              |
| ----------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| router_nameservers                  | yes       | A list of nameservers                                                                                                    |


## Roles

| Role Name                                                                | Description                                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [dhcp](roles/dhcp)                                                       | Deploys a dhcp server                                                                                                           |
| [docker-on-cumulus](roles/docker-on-cumulus)                             | Deploys docker on cumulus                                                                                                       |
| [leaf](roles/leaf)                                                       | Deploys network config for cumulus switches                                                                                     |
| [pixicore](roles/pixicore)                                               | Deploys pixicore                                                                                                                |
| [router](roles/router)                                                   | Deploys router config on cumulus swichtes                                                                                       |

## Examples

An example playbook for deploying the metal-partition with the roles provided by this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
