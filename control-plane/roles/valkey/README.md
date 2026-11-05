# valkey

This role deploys a [valkey](https://valkey.io/) into the control plane. It implements the Redis API, which is required by the metal-apiserver.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# Cron schedule for creating backups.
valkey_backup_restore_sidecar_backup_cron_schedule: '*/3 * * * *'
# Encryption key (32 characters) for encrypting backups.
valkey_backup_restore_sidecar_encryption_key: null
# GCP bucket location for storing backups.
valkey_backup_restore_sidecar_gcp_backup_location: null
# GCP bucket name for storing backups.
valkey_backup_restore_sidecar_gcp_bucket_name: null
# GCP project id of the backup bucket.
valkey_backup_restore_sidecar_gcp_project_id: null
# GCP service account JSON used for accessing the backup bucket.
valkey_backup_restore_sidecar_gcp_serviceaccount_json: null
# Image name of the backup-restore-sidecar.
valkey_backup_restore_sidecar_image_name: null
# Image pull policy for the backup-restore-sidecar container.
valkey_backup_restore_sidecar_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the backup-restore-sidecar.
valkey_backup_restore_sidecar_image_tag: null
# Log level of the backup-restore-sidecar.
valkey_backup_restore_sidecar_log_level: debug
# Maximum amount of backup objects to keep.
valkey_backup_restore_sidecar_object_max_keep: 480
# Backup provider used by the backup-restore-sidecar.
valkey_backup_restore_sidecar_provider: local
# Resource requests and limits for the backup-restore-sidecar container.
valkey_backup_restore_sidecar_resources: null
# S3 access key for the backup bucket.
valkey_backup_restore_sidecar_s3_access_key: null
# S3 bucket name for storing backups.
valkey_backup_restore_sidecar_s3_bucket_name: null
# S3 endpoint of the backup bucket.
valkey_backup_restore_sidecar_s3_endpoint: null
# Whether to skip TLS certificate verification for the S3 endpoint.
valkey_backup_restore_sidecar_s3_insecure_skip_verify: null
# Maximum amount of days to keep a backup object in the bucket.
valkey_backup_restore_sidecar_s3_object_days_max_keep: null
# S3 region of the backup bucket.
valkey_backup_restore_sidecar_s3_region: null
# Controls the RequestChecksumCalculation setting of the S3 client. Either C(when_required) or C(when_supported). Not expressed as C(choices) because the default is unset and choices would reject that.
valkey_backup_restore_sidecar_s3_request_checksum_calculation: null
# S3 secret key for the backup bucket.
valkey_backup_restore_sidecar_s3_secret_key: null
# Trusted CA certificate for the S3 endpoint.
valkey_backup_restore_sidecar_s3_trusted_ca_cert: null
# Security context for the containers.
valkey_container_security_context:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
# Whether to render the pod and container security contexts.
valkey_enable_security_context: true
# Image name of valkey.
valkey_image_name: null
# Image pull policy for the valkey container.
valkey_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of valkey.
valkey_image_tag: null
# Resource requests and limits for the init container.
valkey_init_resources: null
# Name of the valkey deployment.
valkey_name: valkey
# The namespace to deploy valkey to.
valkey_namespace: '{{ metal_control_plane_namespace }}'
# Docker auth configuration for the image pull secret.
valkey_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
valkey_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Resource requests and limits for the valkey container.
valkey_resources:
  # Limits describes the maximum amount of compute resources allowed.
  limits:
    cpu: 800m
    memory: 1Gi
  # Requests describes the minimum amount of compute resources required.
  requests:
    cpu: 400m
    memory: 512M
# Storage class of the persistent volume.
valkey_storage_class: null
# Size of the persistent volume.
valkey_storage_size: 10Gi
# Pod security context for the statefulset.
valkey_sts_security_context:
  fsGroup: 1000
  fsGroupChangePolicy: OnRootMismatch
  runAsGroup: 1000
  runAsNonRoot: true
  runAsUser: 1000
  seccompProfile:
    type: RuntimeDefault
```
