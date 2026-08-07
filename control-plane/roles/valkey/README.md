# valkey

This role deploys a [valkey](https://valkey.io/) into the control plane. It implements the Redis API, which is required by the metal-apiserver.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                                                          | Mandatory | Description                                                                                                            |
| ------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------- |
| valkey_name                                                   |           | The name of the valkey instance                                                                                        |
| valkey_namespace                                              |           | The deployment's target namespace                                                                                      |
| valkey_chart                                                  | yes       | The repository URL of the valkey oci helm chart                                                                        |
| valkey_chart_tag                                              | yes       | The tag of the valkey oci helm chart                                                                                   |
| valkey_image_pull_policy                                      |           | Image pull policy of valkey                                                                                            |
| valkey_replicas                                               |           | The number of deployed replicas                                                                                        |
| valkey_password                                               |           | The password to authenticate with                                                                                      |
| valkey_size                                                   |           | The size of the persistent volume backing the valkey stateful set                                                      |
| valkey_storage_class                                          |           | The storage class used for the persistent volume                                                                       |
| valkey_registry_auth_enabled                                  |           | Enables authentication to registry and sets pull secret                                                                |
| valkey_registry_auth                                          |           | Contains the actual authentication info                                                                                |
| valkey_enable_security_context                                |           | Enables SecurityContext for the valkey StatefulSet and containers                                                      |
| valkey_resources                                              |           | The kubernetes resources for the valkey container                                                                      |
| valkey_init_resources                                         |           | The kubernetes resources for the valkey init container                                                                 |
| valkey_sts_security_context                                   |           | The SecurityContext for the valkey StatefulSet                                                                         |
| valkey_container_security_context                             |           | The SecurityContext for the valkey containers                                                                          |
| valkey_backup_restore_sidecar_resources                       |           | The kubernetes resources for the valkey backup-restore-sidecars container                                              |
| valkey_backup_restore_sidecar_image_pull_policy               |           | Image pull policy (defaults to IfNotPresent)                                                                           |
| valkey_backup_restore_sidecar_provider                        |           | The backup provider. One of `local`, `gcp` or `s3`                                                                     |
| valkey_backup_restore_sidecar_backup_cron_schedule            |           | The backup cron schedule                                                                                               |
| valkey_backup_restore_sidecar_log_level                       |           | The log level of the sidecar                                                                                           |
| valkey_backup_restore_sidecar_gcp_bucket_name                 |           | Bucket name of the GCP bucket                                                                                          |
| valkey_backup_restore_sidecar_gcp_backup_location             |           | Location of the GCP bucket                                                                                             |
| valkey_backup_restore_sidecar_gcp_project_id                  |           | GCP project name                                                                                                       |
| valkey_backup_restore_sidecar_gcp_serviceaccount_json         |           | GCP Serviceaccount JSON string (service account requires bucket access)                                                |
| valkey_backup_restore_sidecar_s3_bucket_name                  |           | The name of the S3 bucket                                                                                              |
| valkey_backup_restore_sidecar_s3_region                       |           | The region where the S3 bucket is located                                                                              |
| valkey_backup_restore_sidecar_s3_endpoint                     |           | The endpoint URL for the S3 storage service                                                                            |
| valkey_backup_restore_sidecar_s3_access_key                   |           | The access key for authenticating with S3                                                                              |
| valkey_backup_restore_sidecar_s3_secret_key                   |           | The secret key for authenticating with S3                                                                              |
| valkey_backup_restore_sidecar_s3_insecure_skip_verify         |           | Skip certificate check of S3 storage service                                                                           |
| valkey_backup_restore_sidecar_s3_trusted_ca_cert              |           | The trusted certificate authority for the S3 storage service                                                           |
| valkey_backup_restore_sidecar_object_max_keep                 |           | The number of objects to keep at the cloud provider bucket                                                             |
| valkey_backup_restore_sidecar_object_days_max_keep            |           | The number of days to keep an object at the cloud provider bucket                                                      |
| valkey_backup_restore_sidecar_s3_request_checksum_calculation |           | Controls the environment variable RequestChecksumCalculation. Possible values are `when_required` and `when_supported` |
| valkey_backup_restore_sidecar_encryption_key                  |           | An optional encryption key to AES-encrypt the backups before uploading them to the backup provider (length == 32)      |
