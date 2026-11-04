# bisdn-config

Prepares a switch running [BISDN Linux](https://www.bisdn.de) for metal-core. metal-core's `bisdn` switcher then renders systemd-networkd files and `frr.conf`; run the [metal-core](../metal-core) role after this one.

It configures what BISDN Linux doesn't set up for a metal-stack leaf by default:

- the hostname, timezone, `resolv.conf` and NTP servers (`systemd-timesyncd`). NTP and DNS are reached through the default route that metal-core leaks from VRF mgmt into the default VRF.
- SSH keys for root.
- `bgpd=yes` in `/etc/frr/daemons`. BISDN's default is `bgpd=no`.
- the management port `enp0` in VRF `mgmt` (networkd files `10-mgmt.netdev`, `10-mgmt.network` and `10-enp0.network`, which metal-core leaves alone).
- sshd bound to VRF `mgmt`, plus `-A INPUT -i mgmt -p tcp --dport 22 -j ACCEPT` ahead of the vendor rule `! -i enp+ --dport 22 -j DROP`. The vendor rule alone drops SSH through the VRF, because netfilter sees the VRF device as the input interface.
- optional port breakouts and FEC (see below).
- the paths above in `/etc/default/user-backup.txt`, so they survive BISDN upgrades.

Moving the management port into VRF mgmt interrupts Ansible's SSH connection once, which is why networkd is reloaded last.

## Port Breakouts and FEC

BISDN Linux has no tool or API for breakouts or FEC. They are set in the Broadcom SDK configuration (`/usr/share/ofdpa/platform/<platform>/config.bcm`), which OF-DPA reads when it starts.

The role installs `bisdn-portconf` and renders `/etc/bisdn-portconf/ports.yaml` from `bisdn_config_breakouts` / `bisdn_config_ports`, which have the same structure as `sonic_config_breakouts` / `sonic_config_ports`. A drop-in for `ofdpa.service` runs `bisdn-portconf` before every ofdpa start, so the configuration is applied again after an upgrade replaced the vendor file. Errors, for example a typo in `ports.yaml`, are logged and never keep ofdpa from starting: it then uses the last generated `config.bcm`.

Applying a change restarts ofdpa and baseboxd, which interrupts the dataplane:

- On first provisioning, when no port configuration was applied before, the role applies it right away.
- Afterwards, it only reports a pending change, unless `bisdn_config_allow_dataplane_restart` is set.

`/etc/bisdn-portconf/portmap.json` lists the netdevs every front panel port becomes. A 4x25G breakout of `port1` gives `port1` plus three new `portN`, for example on AS7726-32X `port35`..`port37`. Use these names in `metal_core_spine_uplinks` and in the partition's switch configuration.

The netdev names after a breakout, the 25G port bitmap and the FEC values are not verified on hardware yet.

The [ztp](../ztp) role can serve the same configuration for first boot (`ztp_bisdn_switches`).

## Variables

| Name                                 | Mandatory                      | Description                                                                                 |
| ------------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------- |
| bisdn_config_mgmt_interface          |                                | The management port, `enp0` by default.                                                     |
| bisdn_config_mgmt_vrf                |                                | Put the management port into VRF mgmt, `true` by default.                                   |
| bisdn_config_mgmt_vrf_table          |                                | Routing table of VRF mgmt, `5000` by default as on SONiC.                                   |
| bisdn_config_mgmt_address            |                                | Address of the management port (CIDR); defaults to its current address.                     |
| bisdn_config_mgmt_gateway            |                                | Default gateway in VRF mgmt; defaults to `metal_partition_mgmt_gateway`.                    |
| bisdn_config_nameservers             |                                | Nameservers for `resolv.conf`.                                                              |
| bisdn_config_ntp_servers             |                                | NTP servers for `systemd-timesyncd`.                                                        |
| bisdn_config_timezone                |                                | Timezone, `Europe/Berlin` by default.                                                       |
| bisdn_config_authorized_keys         |                                | SSH public keys for root.                                                                   |
| bisdn_config_breakouts               |                                | Port breakouts, e.g. `{port1: 4x25G}`.                                                      |
| bisdn_config_ports                   |                                | FEC per port: `default_fec` and `list` of `name`/`fec` (`none`, `rs`, `fc`).                |
| bisdn_config_portconf_url            | with breakouts or ports        | Download URL of `bisdn-portconf`.                                                           |
| bisdn_config_portconf_checksum       | with breakouts or ports        | Checksum of `bisdn-portconf` (`sha256:<hex>`).                                              |
| bisdn_config_allow_dataplane_restart |                                | Restart ofdpa and baseboxd to apply a changed port configuration, `false` by default.       |
