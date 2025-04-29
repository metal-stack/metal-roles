# valkey

This role deploys a [valkey](https://valkey.io/) into the control plane. It implements the Redis API, which is required by the metal-apiserver.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                         | Mandatory | Description                                                       |
| ---------------------------- | --------- | ----------------------------------------------------------------- |
| valkey_namespace             |           | The deployment's target namespace                                 |
| valkey_chart_ref             | yes       | The helm chart reference                                          |
| valkey_chart_version         | yes       | The helm chart version                                            |
| valkey_image_pull_policy     |           | Image pull policy of valkey                                       |
| valkey_replicas              |           | The number of deployed replicas                                   |
| valkey_password              |           | The password to authenticate with                                 |
| valkey_size                  |           | The size of the persistent volume backing the valkey stateful set |
| valkey_storage_class         |           | The storage class used for the persistent volume                  |
| valkey_registry_auth_enabled |           | Enables authentication to registry and sets pull secret           |
| valkey_registry_auth         |           | Contains the actual authentication info                           |
