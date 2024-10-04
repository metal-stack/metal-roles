# headscale

This role deploys a headscale server into the control plane. It is an optional component for deployment and can be used to access firewalls through a VPN mesh such that there is no need for open SSH ports anymore.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

If you want to rotate the API key, you need to delete the `headscale-api-key` secret and re-run the deployment.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `headscale_db_` instead of `postgres_`.

| Name                                           | Mandatory | Description                                                 |
| ---------------------------------------------- | --------- | ----------------------------------------------------------- |
| headscale_image_name                           | yes       | Image name of headscale                                     |
| headscale_image_tag                            | yes       | Image version of headscale                                  |
| headscale_db_image_name                        | yes       | Image name of headscale DB                                  |
| headscale_db_image_tag                         | yes       | Image version of headscale DB                               |
| headscale_db_backup_restore_sidecar_image_name | yes       | Image name of init container for headscale DB               |
| headscale_db_backup_restore_sidecar_image_tag  | yes       | Image version of init container for headscale DB            |
| headscale_noise_private_key                    | yes       | Noise Protocol Private key for TS2021 compatibility         |
| headscale_ingress_dns                          |           | Domain name                                                 |
| headscale_namespace                            |           | The deployment's target namespace                           |
| headscale_tls                                  |           | Enables TLS for headscale                                   |
| headscale_ingress_annotations                  |           | Annotations that will be attached to the ingress resource   |
| headscale_resources                            |           | The kubernetes resources for the actual headscale container |
| headscale_api_key_expiration                   |           | The time how long the generated api key will be valid       |
| headscale_ipv4_prefix                          |           | IPv4 prefix where the tunnel endpoints are created          |
| headscale_ipv6_prefix                          |           | IPv6 prefix where the tunnel endpoints are created          |
