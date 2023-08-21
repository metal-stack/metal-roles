# postgres-backup-restore

Deploys a postgres database together with a [backup-restore-sidecar](https://github.com/metal-stack/backup-restore-sidecar).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                                                    | Mandatory | Description                                                              |
|---------------------------------------------------------|-----------|--------------------------------------------------------------------------|
| postgres_image_name                                     | yes       | Image version of the postgres                                            |
| postgres_image_tag                                      | yes       | Image tag of the postgres                                                |
| postgres_old_image_tag                                  |           | Image tag of the postgres database before the upgrade                    |
| postgres_registry_auth_enabled                          |           | Enables registry authentication                                          |
| postgres_registry_auth                                  |           | The dockerconfigjson content used for registry authentication            |
| postgres_image_pull_policy                              |           | Image pull policy (defaults to IfNotPresent)                             |
| postgres_name                                           |           | The name of the postgres instance                                        |
| postgres_namespace                                      |           | The deployment's target namespace                                        |
| postgres_storage_size                                   |           | The size of the PVC                                                      |
| postgres_storage_class                                  |           | The storage class of the PVC                                             |
| postgres_db                                             |           | The name of the database                                                 |
| postgres_user                                           |           | The user of the postgres database                                        |
| postgres_password                                       |           | The password of the postgres database                                    |
| postgres_max_connections                                |           | The amount of max. connections possible, defaults to 100                 |
| postgres_backup_restore_sidecar_image_name              | yes       | Image version of the backup-restore-sidecar                              |
| postgres_backup_restore_sidecar_image_tag               | yes       | Image tag of the backup-restore-sidecar                                  |
| postgres_backup_restore_sidecar_provider                |           | The backup provider                                                      |
| postgres_backup_restore_sidecar_backup_cron_schedule    |           | The backup cron schedule                                                 |
| postgres_backup_restore_sidecar_log_level               |           | The log level of the sidecar                                             |
| postgres_backup_restore_sidecar_gcp_bucket_name         |           | Bucket name of the GCP bucket                                            |
| postgres_backup_restore_sidecar_gcp_backup_location     |           | Location of the GCP bucket                                               |
| postgres_backup_restore_sidecar_gcp_project_id          |           | GCP project name                                                         |
| postgres_backup_restore_sidecar_gcp_serviceaccount_json |           | GCP Serviceaccount JSON string (service account requires bucket access)  |
| postgres_expose_frontend                                |           | Exposes the postgres over ingress (only use for dev environments)        |
| postgres_ingress_dns                                    |           | The virtual host to reach the postgres frontend when exposed via ingress |
| postgres_resources                                      |           | The kubernetes resources for the actual postgres container               |
| postgres_backup_restore_sidecar_image_pull_policy       |           | Image pull policy (defaults to IfNotPresent)                             |
| postgres_shared_libraries_preload                       |           | Allows setting shared libraries preload configuration                    |
| postgres_shared_buffers                                 |           | Allows setting shared buffer size                                        |
| postgres_maintenance_work_mem                           |           | Allows setting maintenance work memory                                   |
| postgres_work_mem                                       |           | Allows setting work memory                                               |
| postgres_effective_cache_size                           |           | Allows setting effective cache size                                      |
| postgres_backup_restore_sidecar_object_prefix           |           | The prefix to store the object in the cloud provider bucket              |
| postgres_backup_restore_sidecar_object_max_keep         |           | The number of objects to keep at the cloud provider bucket               |

## Major upgrades

Postgres does require special treatment if a major version upgrade is planned. `pg_upgrade` needs to be called with the old and new binaries, also the old data directory and a already initialized data directory which was initialized with the new binary, e.g. `initdb <new directory>`.

To make this process as smooth as possible, backup-restore-sidecar will detect if the version of the database files and the version of the postgres binary differ and will start the upgrade process. Strict validation to ensure all prerequisites are met is done before actually starting the upgrade process.

To trigger such an update you simply raise the version of the postgres container and specify additionally the version of the previous postgres container.

Configuration before the upgrade:

```yaml
...
postgres_image_tag: 12-alpine
...
```

Configuration to trigger the upgrade:

```yaml
...
postgres_image_tag: 15-alpine
postgres_old_image_tag: 12-alpine
...

```

Deploy again With this new configuration and the upgrade process will start, after that the database will run with the new postgres version in place.
You can remove the `postgres_old_image_tag` if you want, but this is not strictly required.