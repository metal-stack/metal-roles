# metal-db

This role provides a database for the metal-api that can be used for storing the main application data.

This role just wraps the [rethinkdb-backup-restore](/control-plane/roles/rethinkdb-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `metal_db_` instead of `rethinkdb_`.

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/metal-roles/control-plane/roles/defaults).

```yaml
# Cron schedule for creating backups.
metal_db_backup_restore_sidecar_backup_cron_schedule: '*/3 * * * *'
# Encryption key (32 characters) for encrypting backups.
metal_db_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
metal_db_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
metal_db_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
metal_db_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
metal_db_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_db_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
metal_db_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_db_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
metal_db_backup_restore_sidecar_log_level: debug
# Maximum age in days of backup objects to keep.
metal_db_backup_restore_sidecar_object_days_max_keep: null
# Maximum amount of backup objects to keep.
metal_db_backup_restore_sidecar_object_max_keep: 480
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
metal_db_backup_restore_sidecar_provider: local
# S3 access key for the backup bucket.
metal_db_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
metal_db_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
metal_db_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
metal_db_backup_restore_sidecar_s3_insecure_skip_verify: null
# S3 region of the backup bucket.
metal_db_backup_restore_sidecar_s3_region: null
# S3 request checksum calculation setting (e.g. when_required for non-AWS S3 endpoints).
metal_db_backup_restore_sidecar_s3_request_checksum_calculation: null
# S3 secret key for the backup bucket.
metal_db_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
metal_db_backup_restore_sidecar_s3_trusted_ca_cert: null
# Whether to expose the RethinkDB web frontend through an ingress.
metal_db_expose_frontend: false
# Image name of the metal db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_db_image_name: null
# Image pull policy for the the metal db container.
metal_db_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the metal db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_db_image_tag: null
# Ingress DNS name for the RethinkDB web frontend.
metal_db_ingress_dns: rethinkdb.{{ metal_control_plane_gateway_dns }}
# Name of the the metal db deployment.
metal_db_name: metal-db
# The namespace to deploy the metal db to.
metal_db_namespace: '{{ metal_control_plane_namespace }}'
# Password of the the metal db database.
metal_db_password: change-me
# Docker auth configuration for the image pull secret.
metal_db_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
metal_db_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the the metal db container.
metal_db_resources:
  limits:
    cpu: 500m
    memory: 4Gi
  requests:
    cpu: 200m
    memory: 2Gi
# Storage class of the persistent volume.
metal_db_storage_class: null
# Size of the persistent volume.
metal_db_storage_size: 5Gi
```
