# metal-core

Deploys metal-core in a systemd-managed Docker container.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                      | Mandatory | Description                                                                                                                                                            |
| ----------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| metal_core_image_name                     | yes       | Image name of metal-core                                                                                                                                               |
| metal_core_image_tag                      | yes       | Image tag of metal-core                                                                                                                                                |
| metal_core_port                           |           | The port that metal-core is listening on                                                                                                                               |
| metal_core_cidr                           |           |                                                                                                                                                                        |
| metal_core_log_level                      |           | The metal-core log level                                                                                                                                               |
| metal_core_rack_id                        | yes       | The rack id describing the rack in which the leaf switches are contained. Can be a logical rack name and is used by the metal-api to identify the switch pair          |
| metal_core_nsq_lookupd_addr               | yes       | The address to the nsq-lookupd that metal-core uses for discovering the NSQ of the metal control plane                                                                 |
| metal_core_nsq_log_level                  |           | The metal-core log level used on NSQ communication                                                                                                                     |
| metal_core_nsq_tls_enabled                |           | Enables tls encryption on NSQ traffic                                                                                                                                  |
| metal_core_nsq_cert_dir                   |           | Defines the path of the NSQ certificates                                                                                                                               |
| metal_core_nsqd_ca_cert                   |           | The CA certificate that signed the NSQ client cert                                                                                                                     |
| metal_core_nsqd_client_cert               |           | The NSQ client certificate                                                                                                                                             |
| metal_core_change_boot_order              |           |                                                                                                                                                                        |
| metal_core_reconfigure_switch             |           | If set to true, metal-core will automatically reconfigure files on the switch                                                                                          |
| metal_core_reconfigure_switch_interval    |           | The interval in which the switch config gets applied from information received from the metal-api                                                                      |
| metal_core_additional_bridge_vids         |           |                                                                                                                                                                        |
| metal_core_additional_bridge_ports        |           |                                                                                                                                                                        |
| metal_core_consider_hosts_file_resolution |           | If set to true mounts `/etc/nsswitch.conf` into the container to enable dns resolution with the hosts file (see [go#22846](https://github.com/golang/go/issues/22846)) |
| metal_core_interfaces_tpl_file            |           | The golang template file to use for rendering `/etc/network/interfaces`. If this is left blank the default template shipped with metal-core will be used. |
| metal_core_frr_tpl_file                   |           | The golang template file to use for rendering `/etc/frr/frr.conf`. If this is left blank the default template shipped with metal-core will be used. |
