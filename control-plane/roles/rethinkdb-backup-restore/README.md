# rethinkdb-backup-restore

Deploys a rethinkdb together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](control-plane). So, make sure you define them adequately as well.

You can look up all the default values [here](defaults/main/main.yaml).

| Name                                                     | Mandatory | Description                                                               |
| -------------------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| rethinkdb_image_name                                     |           | Image version of the rethinkdb                                            |
| rethinkdb_image_tag                                      |           | Image tag of the rethinkdb                                                |
| rethinkdb_name                                           |           | The name of the rethinkdb instance                                        |
| rethinkdb_storage_size                                   |           | The size of the PVC                                                       |
| rethinkdb_password                                       |           | The password of the rethinkdb                                             |
| rethinkdb_backup_restore_sidecar_image_name              |           | Image version of the backup-restore-sidecar                               |
| rethinkdb_backup_restore_sidecar_image_tag               |           | Image tag of the backup-restore-sidecar                                   |
| rethinkdb_backup_restore_sidecar_provider                |           | The backup provider                                                       |
| rethinkdb_backup_restore_sidecar_backup_interval         |           | The backup interval                                                       |
| rethinkdb_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                              |
| rethinkdb_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                                |
| rethinkdb_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                          |
| rethinkdb_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)   |
| rethinkdb_expose_frontend                                |           | Exposes the rethinkdb over ingress (only use for dev environments)        |
| rethinkdb_ingress_dns                                    |           | The virtual host to reach the rethinkdb frontend when exposed via ingress |
| rethinkdb_resources                                      |           | The kubernetes resources for the actual rethinkdb container               |
