# ztp

Configures a server for providing zero-touch-provisioning scripts for switches.

## Variables

| Name                         | Mandatory | Description                                                                                               |
| ---------------------------- | --------- | --------------------------------------------------------------------------------------------------------- |
| ztp_nginx_image_name         | yes       | the docker image to use to serve ztp scripts.                                                             |
| ztp_nginx_image_tag          | yes       | the tag of the docker image to use to serve ztp scripts.                                                  |
| ztp_host_dir_path            |           | the path to serve ztp scripts from.                                                                       |
| ztp_listen_address           |           | the address used to serve ztp requests                                                                    |
| ztp_port                     |           | the port to serve ztp scripts on.                                                                         |
| ztp_authorized_keys          | yes       | the authorized keys that should be installed by ztp.                                                      |
| ztp_admin_user               |           | the user for which the authorized keys will be provisioned.                                               |
| ztp_additional_files         |           | puts additional files into serve directory.                                                               |
| ztp_sonic_nameservers        |           | the nameservers to put into resolv.conf for sonic                                                         |
| ztp_sonic_extended_cacl.ipv4 |           | iptables ipv4 rules that should be added as extended Control Plane ACLs (Edgecore Sonic specific feature) |
| ztp_sonic_extended_cacl.ipv6 |           | iptables ipv6 rules that should be added as extended Control Plane ACLs (Edgecore Sonic specific feature) |

## Provisioning SONiC Switches via ztp.json

On SONiC switches it is possible to describe the ZTP procedure in a file called `ztp.json`.
It contains all steps that should be performed during ZTP along with some additional options.
We use `ztp.json` to trigger a restart of the BGP service after the initial switch provisioning.
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
