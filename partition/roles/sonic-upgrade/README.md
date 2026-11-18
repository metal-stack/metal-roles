# sonic-upgrade

Performs an upgrade of the SONiC OS on a device and reboots it to complete the installation.

It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

```yaml
# The host serving the SONiC image over HTTP. Mutually exclusive with sonic_upgrade_image_path (exactly one must be set).
sonic_upgrade_host: null
# REQUIRED: The filename of the SONiC image to install.
sonic_upgrade_image: null
# The directory on the switch containing the SONiC image. Mutually exclusive with sonic_upgrade_host (exactly one must be set).
sonic_upgrade_image_path: null
# The port used for downloading the image.
sonic_upgrade_port: 8080
# The protocol used for downloading the image.
sonic_upgrade_protocol: http
# The VRF in which the image download is executed.
sonic_upgrade_vrf: mgmt
```
