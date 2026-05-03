# rethinkdb-backup-restore

Deploys a rethinkdb together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                                                     | Mandatory | Description                                                                                                       |
| -------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------- |
| rethinkdb_image_name                                     | yes       | Image version of the rethinkdb                                                                                    |
| rethinkdb_image_tag                                      | yes       | Image tag of the rethinkdb                                                                                        |
| rethinkdb_registry_auth_enabled                          |           | Enables registry authentication                                                                                   |
| rethinkdb_registry_auth                                  |           | The dockerconfigjson content used for registry authentication                                                     |
| rethinkdb_image_pull_policy                              | yes       | Image pull policy (defaults to IfNotPresent)                                                                      |
| rethinkdb_name                                           |           | The name of the rethinkdb instance                                                                                |
| rethinkdb_namespace                                      |           | The deployment's target namespace                                                                                 |
| rethinkdb_storage_size                                   |           | The size of the PVC                                                                                               |
| rethinkdb_storage_class                                  |           | The storage class of the PVC                                                                                      |
| rethinkdb_password                                       |           | The password of the rethinkdb                                                                                     |
| rethinkdb_backup_restore_sidecar_image_name              | yes       | Image version of the backup-restore-sidecar                                                                       |
| rethinkdb_backup_restore_sidecar_image_tag               | yes       | Image tag of the backup-restore-sidecar                                                                           |
| rethinkdb_backup_restore_sidecar_provider                |           | The backup provider. One of `local`, `gcp` or `s3`                                                                |
| rethinkdb_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                                                          |
| rethinkdb_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                                                                      |
| rethinkdb_backup_restore_sidecar_gcp_bucket_name         |           | Bucket name of the GCP bucket                                                                                     |
| rethinkdb_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                                                                        |
| rethinkdb_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                                                                  |
| rethinkdb_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)                                           |
| rethinkdb_backup_restore_sidecar_s3_bucket_name          |           | The name of the S3 bucket                                                                                         |
| rethinkdb_backup_restore_sidecar_s3_region               |           | The region where the S3 bucket is located                                                                         |
| rethinkdb_backup_restore_sidecar_s3_endpoint             |           | The endpoint URL for the S3 storage service                                                                       |
| rethinkdb_backup_restore_sidecar_s3_access_key           |           | The access key for authenticating with S3                                                                         |
| rethinkdb_backup_restore_sidecar_s3_secret_key           |           | The secret key for authenticating with S3                                                                         |
| rethinkdb_backup_restore_sidecar_s3_insecure_skip_verify |           | Skip certificate check of S3 storage service                                                                      |
| rethinkdb_backup_restore_sidecar_s3_trusted_ca_cert      |           | The trusted certificate authority for the S3 storage service                                                      |
| rethinkdb_expose_frontend                                |           | Exposes the rethinkdb over ingress (only use for dev environments)                                                |
| rethinkdb_ingress_dns                                    |           | The virtual host to reach the rethinkdb frontend when exposed via ingress                                         |
| rethinkdb_resources                                      |           | The kubernetes resources for the actual rethinkdb container                                                       |
| rethinkdb_init_resources                                 |           | The kubernetes resources for the rethinkdb init container                                                         |
| rethinkdb_backup_restore_sidecar_resources               |           | The kubernetes resources for the rethinkdb backup-restore-sidecars container                                      |
| rethinkdb_backup_restore_sidecar_image_pull_policy       |           | Image pull policy (defaults to IfNotPresent)                                                                      |
| rethinkdb_backup_restore_sidecar_object_max_keep         |           | The number of objects to keep at the cloud provider bucket                                                        |
| rethinkdb_backup_restore_sidecar_encryption_key          |           | An optional encryption key to AES-encrypt the backups before uploading them to the backup provider (length == 32) |
| rethinkdb_enable_security_context                        |           | Enables SecurityContext for the rethinkdb StatefulSet and containers                                              |
| rethinkdb_sts_security_context                           |           | The SecurityContext for the rethinkdb StatefulSet                                                                 |
| rethinkdb_container_security_context                     |           | The SecurityContext for the rethinkdb Containers                                                                  |
