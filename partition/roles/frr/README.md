# frr

Configures and starts frr.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

| Name                      | Mandatory | Description                                                                                                                                                                                                       |
|---------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| frr_version               |           | The version of FRR to be installed.                                                                                                                                                                               |
| frr_repo                  |           | The repository that contains FRR.                                                                                                                                                                                 |
| frr_conf                  |           | The configuration of FRR to be installed.                                                                                                                                                                         |
| frr_restart_with_networkd |           | If `true`, a systemd drop-in restarts FRR whenever systemd-networkd restarts, until [FRRouting/frr#22383](https://github.com/FRRouting/frr/pull/22383) is merged. Defaults to `false`, which removes the drop-in. |
