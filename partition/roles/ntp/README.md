# ntp

Keeps the clock in sync with systemd-timesyncd. Installing systemd-timesyncd removes chrony or ntp, because the packages conflict.

## Variables

| Name                 | Mandatory | Description                                                     |
|----------------------|-----------|-----------------------------------------------------------------|
| ntp_servers          |           | the ntp servers to sync from (default is ptbtime1-3.ptb.de).    |
| ntp_fallback_servers |           | the servers used when no other is known (default is ptbtime4).  |
