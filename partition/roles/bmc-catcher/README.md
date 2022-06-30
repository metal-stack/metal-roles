# bmc-catcher

Deploys the bmc-catcher that gathers information about DHCP leases for ipmi access to servers.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                          | Mandatory | Description                                                                                             |
|-------------------------------|-----------|---------------------------------------------------------------------------------------------------------|
| bmc_catcher_image_name        | yes       | Image version of the bmc-catcher                                                                        |
| bmc_catcher_image_tag         | yes       | Image tag of the bmc-catcher                                                                            |
| bmc_catcher_bmc_superuser     | yes       | Name of the BMC superuser                                                                               |
| bmc_catcher_bmc_superuser_pwd | yes       | Password of the BMC superuser                                                                           |
| bmc_catcher_nsq_lookupd_addr  | yes       | The address to the nsq-lookupd that bmc-catcher uses for discovering the NSQ of the metal control plane |
| bmc_catcher_nsq_log_level     |           | The metal-core log level used on NSQ communication                                                      |
| bmc_catcher_nsq_tls_enabled   |           | Enables tls encryption on NSQ traffic                                                                   |
| bmc_catcher_nsq_cert_dir      |           | Defines the path of the NSQ certificates                                                                |
| bmc_catcher_nsqd_ca_cert      |           | The CA certificate that signed the NSQ client cert                                                      |
| bmc_catcher_nsqd_client_cert  |           | The NSQ client certificate                                                                              |
| bmc_catcher_console_port      |           | The port where to listen for incoming metal-console connections                                         |
| bmc_catcher_console_ca_cert   |           | The CA certificate for the metal-console port as a string                                               |
| bmc_catcher_console_cert      |           | The certificate for metal-console port as a string                                                      |
| bmc_catcher_console_key       |           | The key for the metal-console port  as a string                                                         |