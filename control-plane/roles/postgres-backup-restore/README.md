# postgres-backup-restore

Deploys a postgres database together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                                    | Mandatory | Description                                                              |
| ------------------------------------------------------- | --------- | ------------------------------------------------------------------------ |
| postgres_image_name                                     |           | Image version of the postgres                                            |
| postgres_image_tag                                      |           | Image tag of the postgres                                                |
| postgres_name                                           |           | The name of the postgres instance                                        |
| postgres_storage_size                                   |           | The size of the PVC                                                      |
| postgres_db                                             |           | The name of the database                                                 |
| postgres_user                                           |           | The user of the postgres database                                        |
| postgres_password                                       |           | The password of the postgres database                                    |
| postgres_backup_restore_sidecar_image_name              |           | Image version of the backup-restore-sidecar                              |
| postgres_backup_restore_sidecar_image_tag               |           | Image tag of the backup-restore-sidecar                                  |
| postgres_backup_restore_sidecar_provider                |           | The backup provider                                                      |
| postgres_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                 |
| postgres_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                             |
| postgres_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                               |
| postgres_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                         |
| postgres_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)  |
| postgres_expose_frontend                                |           | Exposes the postgres over ingress (only use for dev environments)        |
| postgres_ingress_dns                                    |           | The virtual host to reach the postgres frontend when exposed via ingress |
| postgres_resources                                      |           | The kubernetes resources for the actual postgres container               |
