# metal-bmc

Deploys the metal-bmc that gathers information about DHCP leases for ipmi access to servers.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                         | Mandatory | Description                                                                                           |
| ---------------------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| metal_bmc_image_name         | yes       | Image version of the metal-bmc                                                                        |
| metal_bmc_image_tag          | yes       | Image tag of the metal-bmc                                                                            |
| metal_bmc_ipmi_user          | yes       | Name of the IPMI user used for communication with machine BMCs                                        |
| metal_bmc_ipmi_user_pwd      | yes       | Password of the IPMI user used for communication with machine BMCs                                    |
| metal_bmc_nsq_lookupd_addr   | yes       | The address to the nsq-lookupd that metal-bmc uses for discovering the NSQ of the metal control plane |
| metal_bmc_nsq_log_level      |           | The metal-core log level used on NSQ communication                                                    |
| metal_bmc_nsq_tls_enabled    |           | Enables tls encryption on NSQ traffic                                                                 |
| metal_bmc_nsq_cert_dir       |           | Defines the path of the NSQ certificates                                                              |
| metal_bmc_nsqd_ca_cert       |           | The CA certificate that signed the NSQ client cert                                                    |
| metal_bmc_nsqd_client_cert   |           | The NSQ client certificate                                                                            |
| metal_bmc_console_port       |           | The port where to listen for incoming metal-console connections                                       |
| metal_bmc_console_ca_cert    | yes       | The CA certificate for the metal-console port as a string                                             |
| metal_bmc_console_cert       | yes       | The certificate for metal-console port as a string                                                    |
| metal_bmc_console_key        | yes       | The key for the metal-console port  as a string                                                       |
| metal_bmc_console_cert_owner |           | user of the created certificate files                                                                 |
| metal_bmc_console_cert_group |           | group of the created certificate files                                                                |
