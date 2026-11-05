# headscale

This role deploys a headscale server into the control plane. It is an optional component for deployment and can be used to access firewalls through a VPN mesh such that there is no need for open SSH ports anymore.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

If you want to rotate the API key, you need to delete the `headscale-api-key` secret and re-run the deployment.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `headscale_db_` instead of `postgres_`.

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Expiration duration of the created headscale API key.
headscale_api_key_expiration: 365d
# Cron schedule for creating backups.
headscale_db_backup_restore_sidecar_backup_cron_schedule: 0 0 * * *
# Encryption key (32 characters) for encrypting backups.
headscale_db_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
headscale_db_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
headscale_db_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
headscale_db_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
headscale_db_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_db_backup_restore_sidecar_image_name: null
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_db_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
headscale_db_backup_restore_sidecar_log_level: debug
# Object prefix used for backups in the object store.
headscale_db_backup_restore_sidecar_object_prefix: '{{ headscale_db_name }}'
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
headscale_db_backup_restore_sidecar_provider: local
# S3 access key for the backup bucket.
headscale_db_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
headscale_db_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
headscale_db_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
headscale_db_backup_restore_sidecar_s3_insecure_skip_verify: null
# S3 region of the backup bucket.
headscale_db_backup_restore_sidecar_s3_region: null
# S3 secret key for the backup bucket.
headscale_db_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
headscale_db_backup_restore_sidecar_s3_trusted_ca_cert: null
# Name of the headscale database to create.
headscale_db_db: headscale
# Image name of the headscale db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_db_image_name: null
# Image tag of the headscale db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_db_image_tag: null
# Maximum amount of database connections.
headscale_db_max_connections: 250
# Name of the headscale db deployment.
headscale_db_name: headscale-db
# Password of the headscale database.
headscale_db_password: change-me
# Resource requests and limits for the headscale db container.
headscale_db_resources:
  limits:
    cpu: 500m
    memory: 2Gi
  requests:
    cpu: 100m
    memory: 256Mi
# Storage class of the headscale db persistent volume.
headscale_db_storage_class: null
# Size of the headscale db persistent volume.
headscale_db_storage_size: 5Gi
# User of the headscale database.
headscale_db_user: postgres
# Whether to expose headscale through a GatewayAPI HTTPRoute instead of an ingress.
headscale_httproute_enabled: false
# Hostnames for the headscale HTTPRoute.
headscale_httproute_hostnames: []
# HTTPS redirect configuration for the headscale HTTPRoute.
headscale_httproute_https_redirect: {}
# Parent references for the headscale HTTPRoute.
headscale_httproute_parent_refs: []
# Image name of headscale. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_image_name: null
# Image tag of headscale. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
headscale_image_tag: null
# Additional annotations for the headscale ingress.
headscale_ingress_annotations: {}
# Ingress DNS name of headscale.
headscale_ingress_dns: headscale.{{ metal_control_plane_gateway_dns }}
# Whether to create an ingress for headscale.
headscale_ingress_enabled: true
# IPv4 prefix assigned to VPN clients.
headscale_ipv4_prefix: 100.64.0.0/10
# IPv6 prefix assigned to VPN clients.
headscale_ipv6_prefix: fd7a:115c:a1e0::/48
# The namespace to deploy headscale to.
headscale_namespace: '{{ metal_control_plane_namespace }}'
# REQUIRED: The headscale noise protocol private key.
headscale_noise_private_key: null
# Resource requests and limits for the headscale container.
headscale_resources:
  limits:
    cpu: 500m
    memory: 200M
  requests:
    cpu: 100m
    memory: 100M
# Whether TLS is enabled on the headscale ingress.
headscale_tls: true
```
