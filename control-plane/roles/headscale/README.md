# headscale

This role deploys a headscale server into the control plane. It is an optional component for deployment and can be used to access firewalls through a VPN mesh such that there is no need for open SSH ports anymore.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `headscale_db_` instead of `postgres_`.

| Name                          | Mandatory | Description                                                 |
| ----------------------------- | --------- | ----------------------------------------------------------- |
| headscale_image_name          | yes       | Image name of headscale                                     |
| headscale_image_tag           | yes       | Image version of headscale                                  |
| headscale_namespace           |           | The deployment's target namespace                           |
| headscale_tls                 |           | Enables TLS for headscale                                   |
| headscale_ingress_annotations |           | Annotations that will be attached to the ingress resource   |
| headscale_resources           |           | The kubernetes resources for the actual headscale container |
