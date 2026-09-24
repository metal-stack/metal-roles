# mgmt-firewall-rutos

Converges a Teltonika RutOS management firewall (tested against RUTXR1 config exports, `RUTX_R_00.07.24.3`) to a desired
uci state, idempotently. The role reads the device with `uci export`, computes the `uci batch` commands that are still
missing, and does nothing when that list is empty. With the defaults it only shows the commands; nothing is written until
`mgmt_firewall_rutos_apply` is true.

Unlike `mgmt-firewall`, this role is meant to run again and again on a device that is in service, not once on a
factory-reset device.

## How a change is applied

1. Refuse to run when the firmware differs from `mgmt_firewall_rutos_firmware`, when `uci changes` is not empty, or when a
   previous deployment has not finished.
2. Back up every touched package with `uci export` to `mgmt_firewall_rutos_state_dir` on the device.
3. Upload the batch in chunks below dropbear's command length limit (9000 bytes) and stage it with `uci batch`.
4. Export the staged state and compare it with the desired state again. `uci batch` exits 0 even after a parse error, so a
   staged state that does not converge is reverted here and nothing is committed.
5. Start `apply.sh` on the device in the background: commit, `reload_config`, then wait for a confirmation file.
6. Reconnect, read the committed state back, and confirm only if it matches.
7. Without a confirmation within `mgmt_firewall_rutos_confirm_timeout` seconds the device restores the backup with
   `uci import` and reloads again on its own.

Run the deployment from a host whose own connectivity does not depend on the firewall being changed, for example the
management server behind the other firewall of the pair.

```bash
ansible-playbook deploy_mgmt_firewall_rutos.yaml --limit mgmtfw01
ansible-playbook deploy_mgmt_firewall_rutos.yaml --limit mgmtfw01 -e mgmt_firewall_rutos_apply=true
```

## Desired state

`mgmt_firewall_rutos_uci` maps each uci package to its sections. Only the listed packages are read and changed.

```yaml
mgmt_firewall_rutos_uci:
  network:
    purge: [switch_vlan, route]
    purge_anonymous: [interface]
    sections:
      vlan3:
        type: switch_vlan
        options: {device: switch0, vlan: "3", vid: "3", ports: "0t 1"}
  firewall:
    sections:
      "3":
        type: zone
        options: {name: wan, network: [wan, wan_alias]}
  sms_utils:
    sections:
      "@rule[*]":
        options: {enabled: "0"}
  system:
    sections:
      system:
        type: system
        merge: true
        options: {hostname: mgmtfw01}
```

| Key | Meaning |
| --- | --- |
| `sections.<name>` | Named section. Its options are owned: options on the device that are not listed are deleted. |
| `sections.<name>.merge: true` | Only the listed options are enforced, others are left alone. |
| `sections."@type[n]"` | Existing section by index, always merged. Fails if the index does not exist. |
| `sections."@type[*]"` | Every section of that type, always merged. |
| `purge: [types]` | Sections of these types that are not declared are deleted. |
| `purge_anonymous: [types]` | Anonymous sections of these types are deleted, named ones are kept. |
| option value list | Written as a uci list and replaced as a whole. A space-separated string stays an option. |
| option value `null` | The option must be absent. |

Booleans are written as `1`/`0`, numbers as strings. Values must not contain a single quote or a newline.

## Variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `mgmt_firewall_rutos_firmware` | none, mandatory | Content of `/etc/version` the desired state was written for |
| `mgmt_firewall_rutos_uci` | `{}`, mandatory | Desired state, see above |
| `mgmt_firewall_rutos_apply` | `false` | `false` shows the commands only |
| `mgmt_firewall_rutos_state_dir` | `/tmp/mgmt-firewall-rutos` | Backup, batch, `apply.sh` and `apply.log` on the device |
| `mgmt_firewall_rutos_confirm_timeout` | `180` | Seconds the device waits for confirmation before rolling back (estimate, not measured on hardware) |
| `mgmt_firewall_rutos_settle_seconds` | `10` | Seconds between reload and the `applied` marker (estimate) |
| `mgmt_firewall_rutos_reload_command` | `reload_config` | Command run after commit and after a rollback |
| `mgmt_firewall_rutos_reconnect_retries` | `60` | Attempts to read the device back after the reload |
| `mgmt_firewall_rutos_reconnect_delay` | `5` | Seconds between those attempts |
| `mgmt_firewall_rutos_chunk_bytes` | `4000` | Upper bound per uploaded chunk of the batch |

## Tests

`make test` runs `test/uci_test.py` against the filter plugin.
