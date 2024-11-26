# postgres-backup-restore

Deploys a postgres database together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                                    | Mandatory | Description                                                                                                       |
| ------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------- |
| postgres_image_name                                     | yes       | Image version of the postgres                                                                                     |
| postgres_image_tag                                      | yes       | Image tag of the postgres                                                                                         |
| postgres_registry_auth_enabled                          |           | Enables registry authentication                                                                                   |
| postgres_registry_auth                                  |           | The dockerconfigjson content used for registry authentication                                                     |
| postgres_image_pull_policy                              |           | Image pull policy (defaults to IfNotPresent)                                                                      |
| postgres_name                                           |           | The name of the postgres instance                                                                                 |
| postgres_namespace                                      |           | The deployment's target namespace                                                                                 |
| postgres_storage_size                                   |           | The size of the PVC                                                                                               |
| postgres_storage_class                                  |           | The storage class of the PVC                                                                                      |
| postgres_db                                             |           | The name of the database                                                                                          |
| postgres_user                                           |           | The user of the postgres database                                                                                 |
| postgres_password                                       |           | The password of the postgres database                                                                             |
| postgres_max_connections                                |           | The amount of max. connections possible, defaults to 100                                                          |
| postgres_backup_restore_sidecar_image_name              | yes       | Image version of the backup-restore-sidecar                                                                       |
| postgres_backup_restore_sidecar_image_tag               | yes       | Image tag of the backup-restore-sidecar                                                                           |
| postgres_backup_restore_sidecar_provider                |           | The backup provider                                                                                               |
| postgres_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                                                          |
| postgres_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                                                                      |
| postgres_backup_restore_sidecar_gcp_bucket_name         |           | Bucket name of the GCP bucket                                                                                     |
| postgres_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                                                                        |
| postgres_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                                                                  |
| postgres_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)                                           |
| postgres_backup_restore_sidecar_s3_bucket_name          |           | The name of the S3 bucket                                                                                         |
| postgres_backup_restore_sidecar_s3_region               |           | The region where the S3 bucket is located                                                                         |
| postgres_backup_restore_sidecar_s3_endpoint             |           | The endpoint URL for the S3 storage service                                                                       |
| postgres_backup_restore_sidecar_s3_access_key           |           | The access key for authenticating with S3                                                                         |
| postgres_backup_restore_sidecar_s3_secret_key           |           | The secret key for authenticating with S3                                                                         |
| postgres_expose_frontend                                |           | Exposes the postgres over ingress (only use for dev environments)                                                 |
| postgres_ingress_dns                                    |           | The virtual host to reach the postgres frontend when exposed via ingress                                          |
| postgres_resources                                      |           | The kubernetes resources for the actual postgres container                                                        |
| postgres_backup_restore_sidecar_image_pull_policy       |           | Image pull policy (defaults to IfNotPresent)                                                                      |
| postgres_shared_libraries_preload                       |           | Allows setting shared libraries preload configuration                                                             |
| postgres_shared_buffers                                 |           | Allows setting shared buffer size                                                                                 |
| postgres_maintenance_work_mem                           |           | Allows setting maintenance work memory                                                                            |
| postgres_work_mem                                       |           | Allows setting work memory                                                                                        |
| postgres_effective_cache_size                           |           | Allows setting effective cache size                                                                               |
| postgres_backup_restore_sidecar_object_prefix           |           | The prefix to store the object in the cloud provider bucket                                                       |
| postgres_backup_restore_sidecar_object_max_keep         |           | The number of objects to keep at the cloud provider bucket                                                        |
| postgres_backup_restore_sidecar_encryption_key          |           | An optional encryption key to AES-encrypt the backups before uploading them to the backup provider (length == 32) |
