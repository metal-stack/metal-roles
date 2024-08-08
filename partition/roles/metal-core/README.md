# metal-core

Deploys metal-core in a systemd-managed Docker container.

This role can deploy on switches running Cumulus Linux or SONiC. It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                      | Mandatory | Description                                                                                                                                                                |
| ----------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| metal_core_image_name                     | yes       | Image name of metal-core                                                                                                                                                   |
| metal_core_image_tag                      | yes       | Image tag of metal-core                                                                                                                                                    |
| metal_core_cidr                           |           |                                                                                                                                                                            |
| metal_core_log_driver                     |           | The log driver used for the metal-core container log                                                                                                                       |
| metal_core_log_level                      |           | The metal-core log level                                                                                                                                                   |
| metal_core_rack_id                        | yes       | The rack id describing the rack in which the leaf switches are contained. Can be a logical rack name and is used by the metal-api to identify the switch pair              |
| metal_core_reconfigure_switch             |           | If set to true, metal-core will automatically reconfigure files on the switch                                                                                              |
| metal_core_reconfigure_switch_interval    |           | The interval in which the switch config gets applied from information received from the metal-api                                                                          |
| metal_core_grpc_address                   |           | The address (host:port) of the metal-api gRPC server                                                                                                                       |
| metal_core_grpc_cert_dir                  |           | Path to the gRPC certificate files on the host machine                                                                                                                     |
| metal_core_grpc_ca_cert                   |           | The gRPC CA certificate content                                                                                                                                            |
| metal_core_grpc_client_cert               |           | The gRPC client certificate content                                                                                                                                        |
| metal_core_grpc_client_key                |           | The gRPC client certificate key content                                                                                                                                    |
| metal_core_additional_bridge_vids         |           |                                                                                                                                                                            |
| metal_core_additional_bridge_ports        |           |                                                                                                                                                                            |
| metal_core_spine_uplinks                  |           | The switch ports that connect a leaf to a spine switch or other ports that need to be part of the EVPN underlay fabric. Defaults to `swp31` and `swp32` at the metal-core. |
| metal_core_consider_hosts_file_resolution |           | If set to true mounts `/etc/nsswitch.conf` into the container to enable dns resolution with the hosts file (see [go#22846](https://github.com/golang/go/issues/22846))     |
| metal_core_interfaces_tpl_file            |           | The golang template file to use for rendering `/etc/network/interfaces`. If this is left blank the default template shipped with metal-core will be used.                  |
| metal_core_frr_tpl_file                   |           | The golang template file to use for rendering `/etc/frr/frr.conf`. If this is left blank the default template shipped with metal-core will be used.                        |
| metal_core_pxe_vlan_id                    |           | The VLAN ID for the PXE machines. Defaults to `4000`.                                                                                                                      |
| metal_core_additional_volume_mounts       |           |                                                                                                                                                                            |
