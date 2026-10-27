# frr

Configures and starts frr.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

| Name                      | Mandatory | Description                                                                                                                                        |
|---------------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| frr_version               |           | The version of FRR to be installed. Defaults to `8.4`.                                                                                             |
| frr_repo                  |           | The repository that contains FRR. Defaults to `frr-8`.                                                                                             |
| frr_conf                  | yes       | The configuration of FRR to be installed.                                                                                                          |
| frr_restart_with_networkd |           | Restart FRR along with systemd-networkd, a workaround for [FRRouting/frr#22383](https://github.com/FRRouting/frr/pull/22383). Defaults to `false`. |
