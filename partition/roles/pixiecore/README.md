# pixiecore

Deploys pixiecore in a systemd-managed Docker container.

## Variables

| Name                 | Mandatory | Description                                                                                              |
| -------------------- | --------- | -------------------------------------------------------------------------------------------------------- |
| pixiecore_image_name |           | Image version of the pixiecore                                                                           |
| pixiecore_image_tag  | yes       | Image tag of the pixiecore                                                                               |
| pixiecore_api_url    |           | The url the pixiecore server uses in api mode for requesting the boot image. Should point to metal-core. | 
