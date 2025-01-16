# meili-backup-restore

Deploys a meilisearch database together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                                       | Mandatory | Description                                                                                                       |
| ---------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------- |
| meilisearch_image_name                                     | yes       | Image version of the meilisearch                                                                                  |
| meilisearch_image_tag                                      | yes       | Image tag of the meilisearch                                                                                      |
| meilisearch_registry_auth_enabled                          |           | Enables registry authentication                                                                                   |
| meilisearch_registry_auth                                  |           | The dockerconfigjson content used for registry authentication                                                     |
| meilisearch_image_pull_policy                              |           | Image pull policy (defaults to IfNotPresent)                                                                      |
| meilisearch_name                                           |           | The name of the meilisearch instance                                                                              |
| meilisearch_namespace                                      |           | The deployment's target namespace                                                                                 |
| meilisearch_storage_size                                   |           | The size of the PVC                                                                                               |
| meilisearch_storage_class                                  |           | The storage class of the PVC                                                                                      |
| meilisearch_api_key                                        |           | The api key for meilisearch                                                                                       |
| meilisearch_environment                                    |           | Sets the environment configuration for meilisearch                                                                |
| meilisearch_no_analytics                                   |           | Sets the no analytics configuration for meilisearch                                                               |
| meilisearch_backup_restore_sidecar_image_name              | yes       | Image version of the backup-restore-sidecar                                                                       |
| meilisearch_backup_restore_sidecar_image_tag               | yes       | Image tag of the backup-restore-sidecar                                                                           |
| meilisearch_backup_restore_sidecar_provider                |           | The backup provider                                                                                               |
| meilisearch_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                                                          |
| meilisearch_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                                                                      |
| meilisearch_backup_restore_sidecar_gcp_bucket_name         |           | Bucket name of the GCP bucket                                                                                     |
| meilisearch_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                                                                        |
| meilisearch_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                                                                  |
| meilisearch_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)                                           |
| meilisearch_backup_restore_sidecar_s3_bucket_name          |           | The name of the S3 bucket                                                                                         |
| meilisearch_backup_restore_sidecar_s3_region               |           | The region where the S3 bucket is located                                                                         |
| meilisearch_backup_restore_sidecar_s3_endpoint             |           | The endpoint URL for the S3 storage service                                                                       |
| meilisearch_backup_restore_sidecar_s3_access_key           |           | The access key for authenticating with S3                                                                         |
| meilisearch_backup_restore_sidecar_s3_secret_key           |           | The secret key for authenticating with S3                                                                         |
| meilisearch_resources                                      |           | The kubernetes resources for the actual meilisearch container                                                     |
| meilisearch_backup_restore_sidecar_object_max_keep         |           | The number of objects to keep at the cloud provider bucket                                                        |
| meilisearch_backup_restore_sidecar_encryption_key          |           | An optional encryption key to AES-encrypt the backups before uploading them to the backup provider (length == 32) |
