# rethinkdb-backup-restore

Deploys a rethinkdb together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                                     | Mandatory | Description                                                               |
| -------------------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| rethinkdb_image_name                                     | yes       | Image version of the rethinkdb                                            |
| rethinkdb_image_tag                                      | yes       | Image tag of the rethinkdb                                                |
| rethinkdb_registry_auth_enabled                          |           | Enables registry authentication                                           |
| rethinkdb_registry_auth                                  |           | The dockerconfigjson content used for registry authentication             |
| rethinkdb_image_pull_policy                              | yes       | Image pull policy (defaults to IfNotPresent)                              |
| rethinkdb_name                                           |           | The name of the rethinkdb instance                                        |
| rethinkdb_namespace                                      |           | The deployment's target namespace                                         |
| rethinkdb_storage_size                                   |           | The size of the PVC                                                       |
| rethinkdb_storage_class                                  |           | The storage class of the PVC                                              |
| rethinkdb_password                                       |           | The password of the rethinkdb                                             |
| rethinkdb_backup_restore_sidecar_image_name              | yes       | Image version of the backup-restore-sidecar                               |
| rethinkdb_backup_restore_sidecar_image_tag               | yes       | Image tag of the backup-restore-sidecar                                   |
| rethinkdb_backup_restore_sidecar_provider                |           | The backup provider                                                       |
| rethinkdb_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                  |
| rethinkdb_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                              |
| rethinkdb_backup_restore_sidecar_gcp_bucket_name         |           | Bucket name of the GCP bucket                                             |
| rethinkdb_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                                |
| rethinkdb_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                          |
| rethinkdb_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)   |
| rethinkdb_expose_frontend                                |           | Exposes the rethinkdb over ingress (only use for dev environments)        |
| rethinkdb_ingress_dns                                    |           | The virtual host to reach the rethinkdb frontend when exposed via ingress |
| rethinkdb_resources                                      |           | The kubernetes resources for the actual rethinkdb container               |
| rethinkdb_backup_restore_sidecar_image_pull_policy       |           | Image pull policy (defaults to IfNotPresent)                              |
| rethinkdb_backup_restore_sidecar_object_max_keep         |           | The number of objects to keep at the cloud provider bucket                |
