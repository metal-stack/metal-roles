# sonic-upgrade

Performs an upgrade of the Sonic OS on a device and reboots it to complete the installation.

## Variables

| Name                   | Mandatory | Description                                                          |
| ---------------------- | --------- | -------------------------------------------------------------------- |
| sonic_upgrade_vrf      | yes       | The vrf used for pulling the upgrade image                           |
| sonic_upgrade_protocol | yes       | The protocol (http or https) to use when downloading the sonic image |
| sonic_upgrade_host     | yes       | The host from which to dowload the image                             |
| sonic_upgrade_port     | yes       | The port on which the image server listens                           |
| sonic_upgrade_image    | yes       | The file name of the sonic image                                     |
