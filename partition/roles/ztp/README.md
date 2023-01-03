# ZTP

Configures a server for providing zero-touch-provisioning scripts for switches.

## Variables

| Name                   | Mandatory | Description                                               |
| -----------------------| --------- |---------------------------------------------------------- |
| ztp_image_name         | no        | the docker image to use to serve ztp scripts.             |
| ztp_image_tag          | no        | the tag of the docker image to use to serve ztp scripts.  |
| ztp_host_dir_path      | no        | the path to serve ztp scripts from.                       |
| ztp_port               | no        | the port to serve ztp scripts on.                         |
| ztp_authorized_keys    | yes       | the authorized keys that should be installed by ztp.      |
