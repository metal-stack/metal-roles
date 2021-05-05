# bmc-catcher

Deploys the bmc-catcher that gathers information about DHCP leases for ipmi access to servers.

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                          | Mandatory | Description                      |
| ----------------------------- | --------- | -------------------------------- |
| bmc_catcher_image_name        | yes       | Image version of the bmc-catcher |
| bmc_catcher_image_tag         | yes       | Image tag of the bmc-catcher     |
| bmc_catcher_bmc_superuser     | yes       | Name of the BMC superuser        |
| bmc_catcher_bmc_superuser_pwd | yes       | Password of the BMC superuser    |
