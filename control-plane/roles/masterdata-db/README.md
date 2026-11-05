# masterdata-db

This role provides a database for the masterdata-api and tenant-apiserver that can be used for storing the main application data.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `masterdata_db_` instead of `postgres_`.

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/metal-roles/control-plane/roles/defaults).

```yaml
# Cron schedule for creating backups.
masterdata_db_backup_restore_sidecar_backup_cron_schedule: '*/3 * * * *'
# Encryption key (32 characters) for encrypting backups.
masterdata_db_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
masterdata_db_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
masterdata_db_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
masterdata_db_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
masterdata_db_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
masterdata_db_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
masterdata_db_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
masterdata_db_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
masterdata_db_backup_restore_sidecar_log_level: debug
# Maximum age in days of backup objects to keep.
masterdata_db_backup_restore_sidecar_object_days_max_keep: null
# Maximum amount of backup objects to keep.
masterdata_db_backup_restore_sidecar_object_max_keep: 480
# Object prefix used for backups in the object store.
masterdata_db_backup_restore_sidecar_object_prefix: '{{ masterdata_db_name }}-{{ metal_control_plane_stage_name }}'
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
masterdata_db_backup_restore_sidecar_provider: local
# S3 access key for the backup bucket.
masterdata_db_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
masterdata_db_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
masterdata_db_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
masterdata_db_backup_restore_sidecar_s3_insecure_skip_verify: null
# S3 region of the backup bucket.
masterdata_db_backup_restore_sidecar_s3_region: null
# S3 request checksum calculation setting (e.g. when_required for non-AWS S3 endpoints).
masterdata_db_backup_restore_sidecar_s3_request_checksum_calculation: null
# S3 secret key for the backup bucket.
masterdata_db_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
masterdata_db_backup_restore_sidecar_s3_trusted_ca_cert: null
# Name of the database to create.
masterdata_db_db: masterdata
# Image name of the masterdata db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
masterdata_db_image_name: null
# Image pull policy for the the masterdata db container.
masterdata_db_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the masterdata db. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
masterdata_db_image_tag: null
# Maximum amount of database connections.
masterdata_db_max_connections: 100
# Name of the the masterdata db deployment.
masterdata_db_name: masterdata-db
# The namespace to deploy the masterdata db to.
masterdata_db_namespace: '{{ metal_control_plane_namespace }}'
# Password of the the masterdata db database.
masterdata_db_password: change-me
# Docker auth configuration for the image pull secret.
masterdata_db_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
masterdata_db_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the the masterdata db container.
masterdata_db_resources:
  limits:
    cpu: 100m
    memory: 256Mi
  requests:
    cpu: 20m
    memory: 128Mi
# Storage class of the persistent volume.
masterdata_db_storage_class: null
# Size of the persistent volume.
masterdata_db_storage_size: 5Gi
# User of the the masterdata db database.
masterdata_db_user: postgres
```
