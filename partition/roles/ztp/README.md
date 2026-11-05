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

## Installing BISDN Linux via ONIE

BISDN Linux's ONIE installer reads an install config, either as `install.conf` next to the installer or integrated: everything after the installer's final `conf_marker` line. With `ztp_bisdn_installer_url`, this role downloads the installer, checks it against `ztp_bisdn_installer_checksum`, appends an install config and serves the result as `ztp_bisdn_installer_name`. The installer's checksum only covers its payload, so the appended config doesn't invalidate it.

The install config contains:

- `ztp_authorized_keys` for the `basebox` user, so Ansible can log in after the install (see [bisdn-config](../bisdn-config)),
- `ztp_bisdn_password_hash` as basebox's password, if set. It must not contain `=`, because the installer's parser cuts at it: create it without `rounds=`, e.g. with `mkpasswd -m sha-512`.
- `ztp_bisdn_keep_config` as `KEEP_CONFIG`.

BISDN applies keys and password on fresh installs only. A reinstall with `KEEP_CONFIG=true` restores the previous installation's configuration, including its keys.

ONIE fetches the installer from the URL in DHCP option 114, for example with the [dhcp](../dhcp) role:

```yaml
dhcp_static_hosts:
  - name: leaf01
    mac: "aa:aa:aa:aa:aa:aa"
    ip: 10.1.253.154
    options:
      - default-url = "http://10.1.253.13:8080/onie-installer-bisdn"
```

## Port Configuration for BISDN Linux Switches

BISDN Linux has no ZTP client. For switches in `ztp_bisdn_switches`, this role serves `bisdn/<switch>/ports.yaml` (breakouts and FEC, in the structure of `sonic_config_breakouts` / `sonic_config_ports`) and `bisdn-ztp.sh`. Running the script on first boot installs `bisdn-portconf`, applies the port configuration to the Broadcom SDK config (`config.bcm`) and restarts the dataplane once:

```sh
curl -fsS http://10.1.253.13:8080/bisdn-ztp.sh | sh -s leaf01
```

The [bisdn-config](../bisdn-config) role performs the same steps on its first run, so the script is only needed when ports must be broken out before the switch is provisioned.

## Variables

| Name                         | Mandatory | Description                                                 |
| ---------------------------- | --------- | ----------------------------------------------------------- |
| ztp_nginx_image_name         | yes       | the docker image to use to serve ztp scripts.               |
| ztp_nginx_image_tag          | yes       | the tag of the docker image to use to serve ztp scripts.    |
| ztp_nginx_docker_log_driver  |           | Indicates where to write the docker logs to                 |
| ztp_host_dir_path            |           | the path to serve ztp scripts from.                         |
| ztp_listen_address           |           | the address used to serve ztp requests                      |
| ztp_port                     |           | the port to serve ztp scripts on.                           |
| ztp_authorized_keys          | yes       | the authorized keys that should be installed by ztp.        |
| ztp_admin_user               |           | the user for which the authorized keys will be provisioned. |
| ztp_additional_files         |           | puts additional files into serve directory.                 |
| ztp_bisdn_switches           |           | BISDN Linux switches with `breakouts` and `ports` to serve. |
| ztp_bisdn_installer_url      |           | download URL of the BISDN Linux ONIE installer.             |
| ztp_bisdn_installer_checksum |           | checksum of the installer (`sha256:<hex>`).                 |
| ztp_bisdn_installer_name     |           | name the installer is served as.                            |
| ztp_bisdn_password_hash      |           | crypt hash of basebox's password for the install config.    |
| ztp_bisdn_keep_config        |           | `KEEP_CONFIG` of the install config, `true` by default.     |
| ztp_bisdn_portconf_url       |           | download URL of `bisdn-portconf` for BISDN switches.        |
| ztp_bisdn_portconf_checksum  |           | checksum of `bisdn-portconf` (`sha256:<hex>`).              |
