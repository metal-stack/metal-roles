# frr

Configures and starts frr.

This role can deploy on bare metal machines with Debian or Almalinux. It depends on fact gathering.

## Variables

| Name        | Mandatory | Description                         |
| ----------- | --------- | ----------------------------------- |
| frr_version |           | The version of FRR to be installed. |
| frr_repo    |           | The repository that contains FRR.   |
