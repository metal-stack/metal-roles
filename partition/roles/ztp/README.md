# ztp

Configures a server for providing zero-touch-provisioning scripts for switches.

## Variables

| Name                 | Mandatory | Description                                                 |
| -------------------- | --------- | ----------------------------------------------------------- |
| ztp_nginx_image_name | yes       | the docker image to use to serve ztp scripts.               |
| ztp_nginx_image_tag  | yes       | the tag of the docker image to use to serve ztp scripts.    |
| ztp_host_dir_path    |           | the path to serve ztp scripts from.                         |
| ztp_listen_address   |           | the address used to serve ztp requests                      |
| ztp_port             |           | the port to serve ztp scripts on.                           |
| ztp_authorized_keys  | yes       | the authorized keys that should be installed by ztp.        |
| ztp_admin_user       |           | the user for which the authorized keys will be provisioned. |
| ztp_additional_files |           | puts additional files into serve directory.                 |
