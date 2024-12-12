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
The result of this may not be intended and, in the worst case, the switch will reach a broken state from which it only can be restored by a factory reset.
Of course it is also possible to load only a minimal `config_db.json` via ZTP and allow the `sonic` role to render its template based on the `sonic_ports`, `sonic_portchannels` and `sonic_breakouts` variables.
Both approaches have their pros and cons.

### Pros and Cons of Loading a Static config_db.json via ZTP

The main advantage of loading the `config_db.json` once via ZTP and disabling template rendering by the `sonic` role is a better stability and the ability to configure the switch exactly as needed without relying on the complex templating logic in the `sonic` role.
As mentioned above, the problem with loading a new config each time the `sonic` role is run is that even seemingly small changes might break the system (swss crash).
On the other hand, with a ZTP-only approach, since ZTP only runs during initial setup of the switch, the only way of changing the config is by resetting the switch to activate ZTP.
So the desicion of whether to use the `sonic` role's dynamic config or a static ZTP-only config comes down to questions like:

- how often will the config need to change?
- do all ports on the switch look more or less the same or are there ports that require some specific configuration?

In the latter case the templating might run into certain edge cases, where the resulting config breaks the system.
Then you should consider using only a static config.

> For the time being it is up to the user which provisioning procedure they prefer.
> In the future we hope to come up with a single solution that is both flexible and reliable.

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
