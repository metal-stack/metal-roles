# mgmt-firewall-rutos-upgrade

Upgrades the firmware of a Teltonika RutOS management firewall (tested on a RUTXR1 from `RUTX_R_00.07.24.3` to
`RUTX_R_00.07.24.5`) with
`sysupgrade`, keeping the configuration. A device that already runs the requested firmware is left alone. With the
defaults the role only shows the version change and verifies the image; nothing is flashed until
`mgmt_firewall_rutos_upgrade_apply` is true.

## How an upgrade is applied

1. Compare `/etc/version` with `mgmt_firewall_rutos_upgrade_firmware` and stop when they are equal.
2. Refuse to run when `uci changes` is not empty or a deployment of the
   [mgmt-firewall-rutos](../mgmt-firewall-rutos/README.md) role has not finished. `sysupgrade` keeps only committed
   settings.
3. Download the image on the controller and verify it against `mgmt_firewall_rutos_upgrade_sha256`. This proves URL
   and checksum without putting 30 MB into the device's RAM, so it is part of the read-only run.
4. Download the image on the device into `/tmp`, verify the checksum there, and let `sysupgrade -T` check it without
   flashing.
5. Start `sysupgrade` in the background; without `-n` it keeps the configuration. It is started with `&` and
   `trap '' HUP` for the same reason as `apply.sh` in mgmt-firewall-rutos: the flash ends the SSH session that
   started it.
6. Wait from the controller until port 22 closes and opens again, then require `/etc/version` to be the new firmware.

There is no rollback. A firmware that does not boot or does not keep the configuration has to be fixed on the device.
Flash one firewall of a pair at a time, from a host whose own connectivity does not depend on the firewall being
upgraded, for example the management server behind the other firewall.

## Running it

```bash
ansible-playbook upgrade_mgmt_firewall_rutos.yaml --limit mgmtfw01
ansible-playbook upgrade_mgmt_firewall_rutos.yaml --limit mgmtfw01 -e mgmt_firewall_rutos_upgrade_apply=true
```

The first run reads the version, checks the staging area and verifies the image on the controller; the task that shows
the version change reports `changed` when an upgrade is due. The second run flashes.

## Together with mgmt-firewall-rutos

mgmt-firewall-rutos refuses to run on any firmware other than `mgmt_firewall_rutos_firmware`, because a firmware
change can change the defaults and sections its desired state was written against. Point both roles at the same value
in the inventory:

```yaml
mgmt_firewall_rutos_firmware: RUTX_R_00.07.24.5
mgmt_firewall_rutos_upgrade_firmware: "{{ mgmt_firewall_rutos_firmware }}"
mgmt_firewall_rutos_upgrade_sha256: a6c2934b17dbef65280ae595eb935016be8bb4de4fc476b52ba19f33a3c63819
```

Then upgrade, and run mgmt-firewall-rutos read-only. An empty list means the configuration survived the upgrade.
Anything it prints was changed by the firmware and has to be adopted into the inventory or reviewed before it is
applied.

## Variables

| Variable                                   | Default                                | Meaning                                                                  |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------ |
| `mgmt_firewall_rutos_upgrade_firmware`     | none, mandatory                        | Content of `/etc/version` after the upgrade, e.g. `RUTX_R_00.07.24.5`    |
| `mgmt_firewall_rutos_upgrade_sha256`       | none, mandatory                        | SHA256 of the image from Teltonika's RUTX firmware checksum list         |
| `mgmt_firewall_rutos_upgrade_url`          | Teltonika download URL                 | Where controller and device fetch the image                              |
| `mgmt_firewall_rutos_upgrade_apply`        | `false`                                | `false` verifies the image only                                          |
| `mgmt_firewall_rutos_upgrade_image`        | `/tmp/mgmt-firewall-rutos-upgrade.bin` | Image path on the device                                                 |
| `mgmt_firewall_rutos_upgrade_state_dir`    | `/tmp/mgmt-firewall-rutos`             | State directory of mgmt-firewall-rutos, checked for a running deployment |
| `mgmt_firewall_rutos_upgrade_down_timeout` | `300`                                  | Seconds to wait for SSH to close after sysupgrade started (estimate)     |
| `mgmt_firewall_rutos_upgrade_up_timeout`   | `900`                                  | Seconds to wait for SSH to come back after the flash (estimate)          |

The timeouts leave room above a single measurement: on a RUTXR1 upgraded from `RUTX_R_00.07.24.3` to
`RUTX_R_00.07.24.5`, SSH closed 25 s after sysupgrade was started and answered again 283 s later.

The default URL follows the pattern on Teltonika's firmware download pages,
`https://firmware.teltonika-networks.com/7.24.5/RUTX/RUTX_R_00.07.24.5_WEBUI.bin`. Set
`mgmt_firewall_rutos_upgrade_url` to use a mirror; the device needs to reach it as well as the controller.
