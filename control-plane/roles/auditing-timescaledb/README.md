# auditing-timescaledb

This role provides a database for the metal-api that can be used for storing audit traces. The auditing feature has to be explicitly enabled in the metal-api in order to make use of this database.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `auditing_timescaledb_` instead of `postgres_`.

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# Cron schedule for creating backups.
auditing_timescaledb_backup_restore_sidecar_backup_cron_schedule: 0 * * * *
# Encryption key (32 characters) for encrypting backups.
auditing_timescaledb_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
auditing_timescaledb_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
auditing_timescaledb_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
auditing_timescaledb_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
auditing_timescaledb_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
auditing_timescaledb_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
auditing_timescaledb_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
auditing_timescaledb_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
auditing_timescaledb_backup_restore_sidecar_log_level: debug
# Maximum age in days of backup objects to keep.
auditing_timescaledb_backup_restore_sidecar_object_days_max_keep: null
# Maximum amount of backup objects to keep.
auditing_timescaledb_backup_restore_sidecar_object_max_keep: 480
# Object prefix used for backups in the object store.
auditing_timescaledb_backup_restore_sidecar_object_prefix: '{{ auditing_timescaledb_name }}-{{ metal_control_plane_stage_name }}'
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
auditing_timescaledb_backup_restore_sidecar_provider: local
# S3 request checksum calculation setting (e.g. when_required for non-AWS S3 endpoints).
auditing_timescaledb_backup_restore_sidecar_s3_request_checksum_calculation: null
# Name of the database to create.
auditing_timescaledb_db: auditing
# Image name of the auditing timescaledb. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
auditing_timescaledb_image_name: null
# Image pull policy for the the auditing timescaledb container.
auditing_timescaledb_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the auditing timescaledb. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
auditing_timescaledb_image_tag: null
# Maximum amount of database connections.
auditing_timescaledb_max_connections: 100
# Name of the the auditing timescaledb deployment.
auditing_timescaledb_name: auditing-timescaledb
# The namespace to deploy the auditing timescaledb to.
auditing_timescaledb_namespace: '{{ metal_control_plane_namespace }}'
# Password of the the auditing timescaledb database.
auditing_timescaledb_password: change-me
# Docker auth configuration for the image pull secret.
auditing_timescaledb_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
auditing_timescaledb_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the the auditing timescaledb container.
auditing_timescaledb_resources:
  limits:
    cpu: '1'
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 256Mi
# Libraries to preload via shared_preload_libraries.
auditing_timescaledb_shared_libraries_preload:
- pg_stat_statements
- timescaledb
# Storage class of the persistent volume.
auditing_timescaledb_storage_class: null
# Size of the persistent volume.
auditing_timescaledb_storage_size: 10Gi
# User of the the auditing timescaledb database.
auditing_timescaledb_user: postgres
```
