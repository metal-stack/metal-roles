# ztp

Configures a server for providing zero-touch-provisioning scripts for switches.

## Variables

| Name                | Mandatory | Description                                                 |
| ------------------- | --------- | ----------------------------------------------------------- |
| ztp_image_name      |           | the docker image to use to serve ztp scripts.               |
| ztp_image_tag       |           | the tag of the docker image to use to serve ztp scripts.    |
| ztp_host_dir_path   |           | the path to serve ztp scripts from.                         |
| ztp_port            |           | the port to serve ztp scripts on.                           |
| ztp_authorized_keys | yes       | the authorized keys that should be installed by ztp.        |
| ztp_admin_user      |           | the user for which the authorized keys will be provisioned. |
