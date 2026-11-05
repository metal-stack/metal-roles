# postgres-backup-restore

Deploys a postgres database together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Cron schedule for creating backups.
postgres_backup_restore_sidecar_backup_cron_schedule: '*/3 * * * *'
# Encryption key (32 characters) for encrypting backups.
postgres_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
postgres_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
postgres_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
postgres_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
postgres_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
postgres_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
postgres_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
postgres_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
postgres_backup_restore_sidecar_log_level: debug
# Maximum age in days of backup objects to keep.
postgres_backup_restore_sidecar_object_days_max_keep: 14
# Maximum amount of backup objects to keep.
postgres_backup_restore_sidecar_object_max_keep: 480
# Object prefix used for backups in the object store.
postgres_backup_restore_sidecar_object_prefix: '{{ postgres_name }}-{{ metal_control_plane_stage_name }}'
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
postgres_backup_restore_sidecar_provider: local
# Resource requests and limits for the backup-restore-sidecar container.
postgres_backup_restore_sidecar_resources: null
# S3 access key for the backup bucket.
postgres_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
postgres_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
postgres_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
postgres_backup_restore_sidecar_s3_insecure_skip_verify: null
# S3 region of the backup bucket.
postgres_backup_restore_sidecar_s3_region: null
# S3 request checksum calculation setting (e.g. when_required for non-AWS S3 endpoints).
postgres_backup_restore_sidecar_s3_request_checksum_calculation: null
# S3 secret key for the backup bucket.
postgres_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
postgres_backup_restore_sidecar_s3_trusted_ca_cert: null
# Security context for the containers.
postgres_container_security_context:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
# Name of the database to create.
postgres_db: postgres
# PostgreSQL effective_cache_size setting.
postgres_effective_cache_size: null
# Whether to render the pod and container security contexts.
postgres_enable_security_context: false
# Image name of postgres. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
postgres_image_name: null
# Image pull policy for the postgres container.
postgres_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of postgres. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
postgres_image_tag: null
# Resource requests and limits for the init container.
postgres_init_resources: null
# PostgreSQL maintenance_work_mem setting.
postgres_maintenance_work_mem: null
# Maximum amount of database connections.
postgres_max_connections: 100
# Name of the postgres deployment.
postgres_name: postgres
# The namespace to deploy postgres to.
postgres_namespace: '{{ metal_control_plane_namespace }}'
# Password of the postgres database.
postgres_password: change-me
# Docker auth configuration for the image pull secret.
postgres_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
postgres_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the postgres container.
postgres_resources:
  limits:
    cpu: 100m
    memory: 256Mi
  requests:
    cpu: 20m
    memory: 128Mi
# PostgreSQL shared_buffers setting.
postgres_shared_buffers: null
# Libraries to preload via shared_preload_libraries.
postgres_shared_libraries_preload:
- pg_stat_statements
# Storage class of the persistent volume.
postgres_storage_class: null
# Size of the persistent volume.
postgres_storage_size: 5Gi
# Pod security context for the statefulset.
postgres_sts_security_context:
  fsGroup: 2000
  fsGroupChangePolicy: OnRootMismatch
  runAsGroup: 2000
  runAsNonRoot: true
  runAsUser: 1001
  seccompProfile:
    type: RuntimeDefault
# User of the postgres database.
postgres_user: postgres
# PostgreSQL work_mem setting.
postgres_work_mem: null
```
