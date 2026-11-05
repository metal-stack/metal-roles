# rethinkdb-backup-restore

Deploys a rethinkdb together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Cron schedule for creating backups.
rethinkdb_backup_restore_sidecar_backup_cron_schedule: '*/3 * * * *'
# Encryption key (32 characters) for encrypting backups.
rethinkdb_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
rethinkdb_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
rethinkdb_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
rethinkdb_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
rethinkdb_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
rethinkdb_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
rethinkdb_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
rethinkdb_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
rethinkdb_backup_restore_sidecar_log_level: debug
# Maximum age in days of backup objects to keep.
rethinkdb_backup_restore_sidecar_object_days_max_keep: 14
# Maximum amount of backup objects to keep.
rethinkdb_backup_restore_sidecar_object_max_keep: 480
# Backup provider used by the backup-restore-sidecar (local, gcp or s3).
rethinkdb_backup_restore_sidecar_provider: local
# Resource requests and limits for the backup-restore-sidecar container.
rethinkdb_backup_restore_sidecar_resources: null
# S3 access key for the backup bucket.
rethinkdb_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
rethinkdb_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
rethinkdb_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
rethinkdb_backup_restore_sidecar_s3_insecure_skip_verify: null
# S3 region of the backup bucket.
rethinkdb_backup_restore_sidecar_s3_region: null
# S3 request checksum calculation setting (e.g. when_required for non-AWS S3 endpoints).
rethinkdb_backup_restore_sidecar_s3_request_checksum_calculation: null
# S3 secret key for the backup bucket.
rethinkdb_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
rethinkdb_backup_restore_sidecar_s3_trusted_ca_cert: null
# Security context for the containers.
rethinkdb_container_security_context:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
# Whether to render the pod and container security contexts.
rethinkdb_enable_security_context: false
# Whether to expose the RethinkDB web frontend through an ingress.
rethinkdb_expose_frontend: false
# Image name of rethinkdb. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
rethinkdb_image_name: null
# Image pull policy for the rethinkdb container.
rethinkdb_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of rethinkdb. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
rethinkdb_image_tag: null
# Ingress DNS name for the RethinkDB web frontend.
rethinkdb_ingress_dns: rethinkdb.{{ metal_control_plane_gateway_dns }}
# Resource requests and limits for the init container.
rethinkdb_init_resources: null
# Name of the rethinkdb deployment.
rethinkdb_name: rethinkdb
# The namespace to deploy rethinkdb to.
rethinkdb_namespace: '{{ metal_control_plane_namespace }}'
# Password of the rethinkdb database.
rethinkdb_password: change-me
# Docker auth configuration for the image pull secret.
rethinkdb_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
rethinkdb_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the rethinkdb container.
rethinkdb_resources:
  limits:
    cpu: 500m
    memory: 4Gi
  requests:
    cpu: 200m
    memory: 2Gi
# Storage class of the persistent volume.
rethinkdb_storage_class: null
# Size of the persistent volume.
rethinkdb_storage_size: 5Gi
# Pod security context for the statefulset.
rethinkdb_sts_security_context:
  fsGroup: 2000
  fsGroupChangePolicy: OnRootMismatch
  runAsGroup: 2000
  runAsNonRoot: true
  runAsUser: 1001
  seccompProfile:
    type: RuntimeDefault
```
