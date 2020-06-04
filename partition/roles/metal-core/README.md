# metal-core
Deploys metal-core container

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                    | Mandatory | Description                         |
| --------------------------------------- | --------- | ----------------------------------- |
| metal_core_image_name                   |           | Image name of the metal-core        |
| metal_core_image_tag                    | yes       | Image tag of the pixiecore          |
| metal_core_port                         |           |                                     |
| metal_core_cidr                         |           |                                     |
| metal_core_log_level                    |           |                                     |
| metal_core_hmac_key                     |           |                                     |
| metal_core_change_boot_order            |           |                                     |
| metal_core_reconfigure_switch           |           |                                     |
| metal_core_reconfigure_switch_interval  |           |                                     |
| metal_core_image_name                   |           |                                     |
| metal_core_additional_bridge_vids       |           |                                     |
| metal_core_additional_bridge_ports      |           |                                     |
| partition_timezone                      |           | Timezone                            |
| partition_id                            | yes       | Partition id                        |
| partition_rack_id                       | yes       | Rack id                             |
| mgmt_gateway                            | yes       | Management gateway                  |


# metal core nsq

| Name                                    | Mandatory | Description                         |
| --------------------------------------- | --------- | ----------------------------------- |
| metal_core_api_nsq_lookupd              | yes       |                                     |
| metal_core_nsq_log_level                |           |                                     |
| metal_core_nsq_tls_enabled              |           |                                     |
| metal_core_nsq_cert_dir                 |           |                                     |
| metal_core_nsqd_ca_cert                 |           |                                     |
| metal_core_nsqd_client_cert             |           |                                     |


# metal api
| Name                                    | Mandatory | Description                         |
| --------------------------------------- | --------- | ----------------------------------- |
| partition_metal_api_addr                | yes       | Metal API address                   |
| partition_metal_api_port                | yes       | Metal API port                      |
| partition_metal_api_protocol            |           |                                     |
| partition_metal_api_basepath            |           |                                     |
