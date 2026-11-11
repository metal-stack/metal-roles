# bisdn-config

Prepares a switch running [BISDN Linux](https://www.bisdn.de) for metal-core. metal-core's `bisdn` switcher then renders systemd-networkd files and `frr.conf`; run the [metal-core](../metal-core) role after this one.

It configures what BISDN Linux doesn't set up for a metal-stack leaf by default:

- the hostname, timezone (only if BISDN ships its zoneinfo; BISDN Linux 6 has no tzdata and runs in UTC), `resolv.conf` and NTP servers (`systemd-timesyncd`). NTP and DNS are reached through the default route that metal-core leaks from VRF mgmt into the default VRF.
- SSH keys for root.
- `bgpd=yes` in `/etc/frr/daemons`. BISDN's default is `bgpd=no`.
- `docker.service` enabled and started. BISDN ships Docker but leaves it disabled, and the metal-core role runs metal-core as a Docker container.
- the management port in VRF `mgmt` (networkd files `10-mgmt.netdev`, `10-mgmt.network` and `10-<port>.network`, which metal-core leaves alone). The port is the `enp*` netdev with an IPv4 address: `enp0` on most platforms, `enp11s0` on the AS7726-32X.
- sshd bound to VRF `mgmt`, plus `-A INPUT -i mgmt -p tcp --dport 22 -j ACCEPT` ahead of the vendor rule `! -i enp+ --dport 22 -j DROP`. The vendor rule alone drops SSH through the VRF, because netfilter sees the VRF device as the input interface.
- optional port breakouts and FEC (see below).
- the paths above in `/etc/default/user-backup.txt`, so they survive BISDN upgrades.

Moving the management port into VRF mgmt interrupts Ansible's SSH connection once. The switch applies the change in one detached step (reload networkd, wait for the VRF device, restart `sshd.socket`), and the role waits for SSH through VRF mgmt.

## Initial Access

Ansible needs SSH access before this role can run. On a fresh install, BISDN's ONIE installer applies its integrated install config, which the [ztp](../ztp) role builds into the installer it serves (`ztp_bisdn_installer_url`). The install config puts `ztp_authorized_keys` into `/home/basebox/.ssh/authorized_keys` and, with `ztp_bisdn_password_hash`, sets basebox's password.

Ansible therefore connects as `basebox` with that key (`ansible_user: basebox`, `become: true`):

- **First run:** BISDN's sudoers asks basebox for a password, so give the become password once (`--ask-become-pass` or `ansible_become_password`). Use the password behind `ztp_bisdn_password_hash`, or BISDN's default password if none was set. The default is publicly known, so set `ztp_bisdn_password_hash`.
- **Later runs:** this role installs `/etc/sudoers.d/zz-metal-stack` with `basebox ALL=(ALL) NOPASSWD: ALL` (`bisdn_config_basebox_nopasswd_sudo`, `true` by default, validated with `visudo`), so no become password is needed anymore. The name sorts after BISDN's own `basebox` drop-in (`basebox ALL=(ALL) ALL`), because sudo applies the last matching rule.

The role also installs root's keys (`bisdn_config_authorized_keys`) for metal-core's management access.

## Port Breakouts and FEC

BISDN Linux has no tool or API for breakouts. They are set in the Broadcom SDK configuration (`/usr/share/ofdpa/platform/<platform>/config.bcm`), which OF-DPA reads when it starts. FEC is set with Broadcom shell commands in `/etc/ofdpa/rc.soc`, which OF-DPA runs when it starts ([BISDN docs](https://docs.bisdn.de/platform_configuration/forward_error_correction.html)).

- **Breakouts:** the role installs BISDN's `ofdpa-breakout` ([files/ofdpa-breakout](files/ofdpa-breakout), MIT, with a fix for more than one breakout) and renders `/etc/ofdpa/breakout.conf` from `bisdn_config_breakouts`. A drop-in for `ofdpa.service` runs `ofdpa-breakout apply` before every ofdpa start. It keeps the vendor file as `config.bcm.dist` and generates `config.bcm` again after an upgrade replaced it. Errors are logged and never keep ofdpa from starting: it then uses the last generated `config.bcm`. Upstream, BISDN tracks a runtime split in bisdn/bisdn-linux#171.
- **FEC:** the role renders `/etc/ofdpa/rc.soc` from `bisdn_config_ports` with one `phy control <n> <clause>=true` per port, where `<n>` is the front panel number of `port<n>`. RS-FEC is clause 91 at 100G and clause 108 at 25G, FC-FEC is clause 74. The role takes each port's speed from the generated `config.bcm`. `none` needs no line, because Broadcom switches start without FEC.

### Input

`bisdn_config_breakouts` and `bisdn_config_ports` have the structure of `sonic_config_breakouts` / `sonic_config_ports`, with BISDN port names:

```yaml
bisdn_config_breakouts:
  port1: 1x100G[40G]     # stays as it is
  port4: 4x25G
  port5: 4x25G
bisdn_config_ports:
  default_fec: none
  list:
    - name: port1
      fec: rs
    - name: port35       # a lane of the port4 breakout
      fec: rs
    - name: port31       # without fec: default_fec
```

`bisdn_config_breakouts` maps a front panel port to a breakout mode:

| Key       | Value                                          |
| --------- | ---------------------------------------------- |
| `port<N>` | Name of the port before the breakout, `N` ≥ 1. |
| mode      | One of the breakout modes below.               |

`bisdn_config_ports` sets FEC:

| Field         | Mandatory | Value                                                                                |
| ------------- | --------- | ------------------------------------------------------------------------------------ |
| `default_fec` |           | FEC mode for every port whose lane speed supports it, `none` by default.             |
| `list`        |           | Ports that differ from the default.                                                  |
| `list[].name` | yes       | A front panel port after the breakouts, including the new lanes (`port35`, ...).     |
| `list[].fec`  |           | FEC mode of that port; `default_fec` if left out. It must fit the port's lane speed. |

Other keys are rejected, so a typo fails instead of being ignored.

### Allowed Values

[filter_plugins/bisdn_ports.py](filter_plugins/bisdn_ports.py) validates the input, and its dictionaries `BREAKOUT_MODES`, `UNCHANGED` and `FEC_CLAUSES` are the source of these tables. Change the README together with them.

Breakout modes (`BREAKOUT_MODES`, `UNCHANGED`):

| Mode                        | Result                                                                |
| --------------------------- | --------------------------------------------------------------------- |
| `4x25G`                     | Four 25G lanes.                                                       |
| `4x10G`                     | Four 10G lanes.                                                       |
| `1x<speed>G`, `1x100G[40G]` | No breakout, the port stays as it is (as in SONiC's breakout tables). |
| anything else               | Rejected.                                                             |

`ofdpa-breakout` also rejects ports that aren't 4-lane ports on the platform, for example the SFP+ ports.

FEC modes and the clause per lane speed (`FEC_CLAUSES`), taken from the port speeds in the generated `config.bcm`:

| Mode   | 100G   | 25G     | 10G    |
| ------ | ------ | ------- | ------ |
| `none` | –      | –       | –      |
| `rs`   | `cl91` | `cl108` | –      |
| `fc`   | –      | `cl74`  | `cl74` |

`none` needs no line in `rc.soc`, because Broadcom switches start without FEC. `default_fec` skips ports where its mode has no clause (`rs` on the 10G SFP+ ports, for example). A mode set in `list` at such a speed is rejected.

### Applying

Breakouts and FEC take effect when the switch reboots. Restarting ofdpa and baseboxd is not enough for a breakout. A reboot interrupts the dataplane:

- On first provisioning, when no port configuration was applied before, the role reboots the switch right away.
- Afterwards, it only reports a pending change, unless `bisdn_config_allow_reboot` is set.

`/etc/ofdpa/metal-stack-applied` records the applied breakouts and FEC settings, so a run that fails before the reboot leaves the change pending.

A 4x25G breakout keeps the parent's name for the first lane. The other three lanes get the next free numbers after the highest port, in front panel order. On the AS7726-32X (34 ports), `port4`..`port10` split into 4x25G give `port4`, `port35`..`port37` up to `port10`, `port53`..`port55`. OF-DPA numbers the ports consecutively, so splitting a lower port later renumbers the lanes of higher ones. Use these names in `bisdn_config_ports`, `metal_core_spine_uplinks` and the partition's switch configuration.

Verified on an AS7726-32X with BISDN Linux 6.0.0: 4x25G on `port4`..`port10` (28 lanes at 25G in the SDK) and RS-FEC (CL91) on `port1`..`port3`.

The [ztp](../ztp) role can serve the same breakouts for first boot (`ztp_bisdn_switches`).

## Variables

| Name                               | Mandatory | Description                                                                                   |
| ---------------------------------- | --------- | --------------------------------------------------------------------------------------------- |
| bisdn_config_mgmt_interface        |           | The management port; defaults to the `enp*` port with an IPv4 address, else `enp0`.           |
| bisdn_config_mgmt_vrf              |           | Put the management port into VRF mgmt, `true` by default.                                     |
| bisdn_config_mgmt_vrf_table        |           | Routing table of VRF mgmt, `5000` by default as on SONiC.                                     |
| bisdn_config_mgmt_address          |           | Address of the management port (CIDR); defaults to its current address.                       |
| bisdn_config_mgmt_gateway          |           | Default gateway in VRF mgmt; defaults to `metal_partition_mgmt_gateway`.                      |
| bisdn_config_nameservers           |           | Nameservers for `resolv.conf`.                                                                |
| bisdn_config_ntp_servers           |           | NTP servers for `systemd-timesyncd`.                                                          |
| bisdn_config_timezone              |           | Timezone, `Europe/Berlin` by default; skipped if BISDN has no zoneinfo for it.                |
| bisdn_config_authorized_keys       |           | SSH public keys for root.                                                                     |
| bisdn_config_basebox_nopasswd_sudo |           | Let basebox use sudo without a password, `true` by default.                                   |
| bisdn_config_breakouts             |           | Port breakouts, e.g. `{port4: 4x25G}`, see [Port Breakouts and FEC](#port-breakouts-and-fec). |
| bisdn_config_ports                 |           | FEC per port (`default_fec`, `list`), see [Port Breakouts and FEC](#port-breakouts-and-fec).  |
| bisdn_config_allow_reboot          |           | Reboot the switch to apply a changed port configuration, `false` by default.                  |
| bisdn_config_reboot_timeout        |           | Seconds to wait for the switch to come back after that reboot, `900` by default.              |
