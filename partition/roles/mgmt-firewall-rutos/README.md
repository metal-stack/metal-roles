# mgmt-firewall-rutos

Converges a Teltonika RutOS management firewall (tested against RUTXR1 config exports, `RUTX_R_00.07.24.3`) to a desired
uci state, idempotently. The role reads the device with `uci export`, computes the `uci batch` commands that are still
missing, and does nothing when that list is empty. With the defaults it only shows the commands; nothing is written until
`mgmt_firewall_rutos_apply` is true.

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

## Running it

A change is deployed in two runs of the same playbook, one firewall at a time.

The first run is read-only. It exports the device, computes the uci commands that are still missing and prints them;
the task that prints them reports `changed` when the list is not empty. Nothing is written to the device, so this run is
safe at any time, also as a drift check in CI.

```bash
ansible-playbook deploy_mgmt_firewall_rutos.yaml --limit mgmtfw01
```

Review the printed commands. If they are what you expect, run again with `mgmt_firewall_rutos_apply=true` to apply
them as described above. This run reads the device again and applies the list it computes then; if someone changed the
device in between, that list differs from the one you reviewed, and it is printed again before anything is written.

```bash
ansible-playbook deploy_mgmt_firewall_rutos.yaml --limit mgmtfw01 -e mgmt_firewall_rutos_apply=true
```

A further read-only run afterwards prints an empty list. Run both from a host whose own connectivity does not depend on
the firewall being changed, for example the management server behind the other firewall of the pair: if the change cuts
that host off, it cannot confirm, and the device rolls back.

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

The format is specific to this role. For the uci model underneath it (packages, named and anonymous sections, options
and lists) see the [OpenWrt uci documentation](https://openwrt.org/docs/guide-user/base-system/uci) and Teltonika's
[UCI command usage](https://wiki.teltonika-networks.com/view/UCI_command_usage). The quickest way to write a desired
state is to start from `uci export <package>` on a device configured through the WebUI and copy the sections over.

### A pair of management firewalls

The state both firewalls share goes into the group, the addresses into each host, and the two are combined with
`combine(recursive=True)`. `recursive` merges the section maps; a list such as `purge` or `src_ip` is replaced, not
appended, so a host that sets it must repeat the whole list.

`group_vars/mgmtfirewalls/mgmt-firewall-rutos.yaml`:

```yaml
mgmt_firewall_rutos_firmware: RUTX_R_00.07.24.3
mgmt_firewall_rutos_uci: "{{ mgmt_firewall_rutos_uci_common | combine(mgmt_firewall_rutos_uci_host, recursive=True) }}"
mgmt_firewall_rutos_uci_host: {}
mgmt_firewall_rutos_uci_common:
  network:
    purge: [switch_vlan, route]
    purge_anonymous: [interface]
    sections:
      vlan4:
        type: switch_vlan
        options: {device: switch0, vlan: "4", vid: "4", ports: "0t 2"}
  firewall:
    purge: [redirect]
    sections:
      "1":
        type: defaults
        options:
          input: DROP
          output: ACCEPT
          forward: DROP
          syn_flood: true
          drop_invalid: true
      "2":
        type: zone
        options:
          name: lan
          input: ACCEPT
          output: ACCEPT
          forward: ACCEPT
          network: lan mgmtsrv
      "3":
        type: zone
        options:
          name: wan
          input: DROP
          output: ACCEPT
          forward: DROP
          masq: true
          mtu_fix: true
          network: wan
      "4":
        type: forwarding
        options: {src: lan, dest: wan}
      "15":
        type: rule
        options:
          name: Enable_SSH_WAN
          src: wan
          proto: tcp
          dest_port: ["22"]
          src_ip: [198.51.100.10, 198.51.100.11]
          target: ACCEPT
          enabled: true
          family: null
  dropbear:
    sections:
      "@dropbear[0]":
        options: {enable_key_ssh: "1"}
  uhttpd:
    sections:
      main:
        type: uhttpd
        merge: true
        options: {redirect_https: "0"}
  sms_utils:
    sections:
      "@rule[*]":
        options: {enabled: "0"}
```

`host_vars/mgmtfw01.yaml`:

```yaml
mgmt_firewall_rutos_uci_host:
  network:
    sections:
      wan:
        type: interface
        options:
          proto: static
          device: eth1
          ipaddr: 203.0.113.36
          netmask: 255.255.255.248
          gateway: 203.0.113.33
          dns: [1.1.1.1, 1.0.0.1]
          peerdns: false
          metric: "1"
      mgmtsrv:
        type: interface
        options:
          proto: static
          device: eth0.4
          ipaddr: 10.1.253.1
          netmask: 255.255.255.252
          force_link: true
      "7":
        type: route
        options:
          interface: mgmtsrv
          target: 10.1.0.0
          netmask: 255.255.0.0
          gateway: 10.1.253.2
  firewall:
    sections:
      ssh_mgmtsrv:
        type: redirect
        options:
          name: ssh_mgmtsrv
          src: wan
          src_dip: 203.0.113.36
          src_dport: "2222"
          src_ip: [198.51.100.10, 198.51.100.11]
          dest: lan
          dest_ip: 10.1.253.2
          dest_port: "22"
          proto: [tcp]
          target: DNAT
  system:
    sections:
      system:
        type: system
        merge: true
        options: {hostname: mgmtfw01}
```

What a run does with this, package by package:

- **network**: `wan`, `mgmtsrv` and `vlan4` are owned, so an option added in the WebUI is deleted again. Every other
  `switch_vlan` and `route` is deleted, and so is every anonymous `interface`; named interfaces that are not declared, such as
  `lan`, stay. `dns` is a list and is rewritten whenever its content or order differs.
- **firewall**: on RutOS these sections carry numbers as names in `uci export`, so `"1"` to `"15"` are names, not
  indexes, and need quotes in YAML. `family: null` removes the option if present. Every redirect other than
  `ssh_mgmtsrv` is deleted; `rule` is not purged, so the firmware's own rules stay untouched.
- **dropbear**: the section is anonymous, so it is addressed by index. That is only allowed because no `dropbear`
  section is created or purged in the same run; otherwise the index could shift and the role refuses.
- **uhttpd**, **system**: `merge: true` enforces a single option in a section full of firmware defaults.
- **sms_utils**: every `rule` is disabled, however many the firmware ships.

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
