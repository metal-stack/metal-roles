# ntp

Keeps the clock in sync with systemd-timesyncd. Installing systemd-timesyncd removes chrony or ntp, because the packages conflict.

## Variables

| Name                 | Mandatory | Description                                                                            |
|----------------------|-----------|----------------------------------------------------------------------------------------|
| ntp_servers          | yes       | the ntp servers to sync from.                                                          |
| ntp_fallback_servers |           | the servers used when no other is known; if empty, the distribution's default applies. |
