# ztp

Configures a server for providing zero-touch-provisioning scripts for switches.

## Provisioning SONiC Switches via ztp.json

On SONiC switches it is possible to describe the ZTP procedure in a file called `ztp.json`.
It contains all steps that should be performed during ZTP along with some additional options.
For example, host-specific download paths for the `config_db.json` or any additional files or scripts can be provided in the `ztp.json`.
To use the `ztp.json` file, add a DHCP option with code 67 to the DHCP server that serves the file.
For example, add a section like the following to `/etc/dhcp/dhcpd.conf`:

```plain
option sonic_ztp code 67 = text;

host leaf01 {
  hardware ethernet aa:aa:aa:aa:aa:aa;
  fixed-address 10.1.253.154;
  option sonic_ztp "http://10.1.253.13:8080/ztp.json";
}
```

For more information on the `ztp.json` format refer to the [documentation](https://github.com/sonic-net/SONiC/blob/master/doc/ztp/ztp.md).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../defaults/README.md).

```yaml
# Additional files (name, data) to serve. Must not contain a file named user.sh.
ztp_additional_files: []
# The admin user created during provisioning.
ztp_admin_user: admin
# REQUIRED: The authorized_keys content installed for the admin user during provisioning.
ztp_authorized_keys: null
# Host directory from which the ZTP files are served.
ztp_host_dir_path: /ztp
# The address on which the ZTP files are served.
ztp_listen_address: '{{ ansible_host }}'
# Docker log driver for the nginx container.
ztp_nginx_docker_log_driver: json-file
# Image name of nginx. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
ztp_nginx_image_name: null
# Image tag of nginx. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
ztp_nginx_image_tag: null
# The port on which the ZTP files are served.
ztp_port: 8080
```
