# ztp

Configures a server for providing zero-touch-provisioning scripts for switches.

## Provisioning SONiC Switches via ztp.json

On SONiC switches it is possible to describe the ZTP procedure in a file called `ztp.json`.
It contains all steps that should be performed during ZTP along with some additional options.
For example, host-specific download paths for the `config_db.json` or any additional files or scripts can be provided in the `ztp.json`.
To use the `ztp.json` file, add a DHCP option with code 67 to the DHCP server that serves the file.
For example, add a section like the following to `/etc/dhcp/dhcpd.conf`:

```
option sonic_ztp code 67 = text;

host leaf01 {
  hardware ethernet aa:aa:aa:aa:aa:aa;
  fixed-address 10.1.253.154;
  option sonic_ztp "http://10.1.253.13:8080/ztp.json";
}
```

For more information on the `ztp.json` format refer to the [documentation](https://github.com/sonic-net/SONiC/blob/master/doc/ztp/ztp.md).

Note that each switch that uses the `ztp.json` file needs an individual `config_db.json`, that it can download at `http://{{ ztp_listen_address }}:{{ ztp_port }}/<hostname>_config_db.json`.
For example, if the switch's hostname is `r01leaf02`, there should be a file called `r01leaf02_config_db.json` located in `{{ ztp_host_dir_path }}/config/`.
The configs can be added to the `ztp_additional_files` variable, e.g.

```yaml
ztp_additional_files:
  - name: r01leaf02_config_db.json
    data: "{{ lookup('file', 'path/to/r01leaf02_config_db.json)' | string }}" # using `string` to keep the formatting
  - name: r02leaf01_config_db.json
    data: ...
```

When a SONiC switch is deployed via `ztp.json` and configured by the `sonic` role afterwards, make sure to leave the `sonic_ports`, `sonic_portchannels` and `sonic_breakouts` variables empty and set `sonic_render_config_db_template` to false.
Otherwise the `sonic` role will override the `config_db.json` provided by the `ztp.json`.
The result of this is unpredictable and, in the worst case, the switch might reach a broken state from which it can only be restored by resetting it completely and setting it up from scratch.

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
