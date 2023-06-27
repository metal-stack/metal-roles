# sonic-upgrade

Performs an upgrade of the SONiC OS on a device and reboots it to complete the installation.

## Variables

| Name                     | Mandatory | Description                                                                                                         |
| ------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------- |
| sonic_upgrade_host       | yes       | The host from which to dowload the image.                                                                           |
| sonic_upgrade_image_path |           | The path to the image. If this is given and not `sonic_upgrade_host`, the image is pushed to the device by ansible. |
| sonic_upgrade_vrf        |           | The vrf used for pulling the upgrade image.                                                                         |
| sonic_upgrade_protocol   |           | The protocol (http or https) to use when downloading the sonic image.                                               |
| sonic_upgrade_port       |           | The port on which the image server listens.                                                                         |
| sonic_upgrade_image      | yes       | The file name of the sonic image.                                                                                   |
