# metal

This role basically deploys the `metal-control-plane` [helm chart](https://github.com/metal-stack/helm-charts/tree/master/charts/metal-control-plane). It uses [hooks](https://github.com/helm/helm/blob/master/docs/charts_hooks.md) to deploy the control plane. There is a post-install hook to initialize the rethinkdb tables (there would be race conditions if there are multiple metal-api replicas initializing the database at the same time). Then, there are post-install and post-upgrade hooks to initialize and update the "masterdata" of the control plane (e.g. images, partitions, networks in this control plane).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

### General

| Name                            | Mandatory | Description                                                                                              |
|---------------------------------|-----------|----------------------------------------------------------------------------------------------------------|
| metal_check_api_available       |           | Checks whether the metal-api is reachable from the outside after deployment                              |
| metal_check_api_health_endpoint |           | The endpoint to call if the metal-api is reachable from the outside after deployment                     |
| metal_set_resource_limits       |           | Deploys metal components with or without resource limits (possibly disable for development environments) |
| metal_log_level                 |           | The log level of the control plane components                                                            |
| metal_helm_chart_repo           |           | The repository URL of the metal control plane helm chart                                                 |
| metal_helm_chart_version        |           | The version of the metal control plane helm chart                                                        |
| metal_helm_chart_local_path     |           | Local path to the metal control plane helm chart, which can be useful for development purposes           |
| metal_helm_chart_timeout        |           | Timeout for deploying the control plane helm chart (can help when internet connection is slow)           |

### Images

| Name                                   | Mandatory | Description                              |
| -------------------------------------- | --------- | ---------------------------------------- |
| metal_api_image_name                   | yes       | Image version of the metal-api           |
| metal_api_image_tag                    | yes       | Image tag of the metal-api               |
| metal_api_image_pull_policy            |           | Image pull policy of the metal-api       |
| metal_apiserver_image_tag              | yes       | Image version of the metal-apiserver     |
| metal_apiserver_url                    | yes       | Image tag of the metal-apiserver         |
| metal_apiserver_image_pull_policy      |           | Image pull policy of the metal-apiserver |
| metal_metalctl_image_name              | yes       | Image version of metalctl                |
| metal_metalctl_image_tag               | yes       | Image tag of metalctl                    |
| metal_metalctl_image_pull_policy       |           | Image pull policy of metalctl            |
| metal_console_image_name               | yes       | Image version of the metal-console       |
| metal_console_image_tag                | yes       | Image tag of the metal-console           |
| metal_console_image_pull_policy        |           | Image pull policy of the metal-console   |
| metal_masterdata_api_image_name        | yes       | Image version of the masterdata-api      |
| metal_masterdata_api_image_tag         | yes       | Image tag of the masterdata-api          |
| metal_masterdata_api_image_pull_policy |           | Image pull policy of the masterdata-api  |
| metal_ipam_image_name                  | yes       | Image version of the ipam                |
| metal_ipam_image_tag                   | yes       | Image tag of the ipam                    |

### Service Ports

| Name                              | Mandatory | Description                                       |
|-----------------------------------|-----------|---------------------------------------------------|
| metal_api_port                    |           | Service port of the metal-api                     |
| metal_api_metrics_port            |           | Service port of the metal-api metrics server      |
| metal_masterdata_api_port         |           | Service port of the masterdata-api                |
| metal_masterdata_api_metrics_port |           | Service port of the masterdata-api metrics server |
| metal_console_port                |           | Service port of the metal-console                 |

### metal-api

| Name                                | Mandatory | Description                                                                                    |
| ----------------------------------- | --------- | ---------------------------------------------------------------------------------------------- |
| metal_api_replicas                  |           | The number of deployed replicas of the metal-api                                               |
| metal_api_hpa_enabled               |           | Enables horizontal pod autoscaling for the metal-api                                           |
| metal_api_hpa_max                   |           | Max amount of replicas for the HPA of the metal-api                                            |
| metal_api_hpa_min                   |           | Min amount of replicas for the HPA of the metal-api                                            |
| metal_api_hpa_cpu_percentage        |           | Target CPU utilization percentage for the HPA of the metal-api                                 |
| metal_api_base_path                 |           | The base path of the HTTP server                                                               |
| metal_api_dex_address               |           | The URL to the dex server                                                                      |
| metal_api_dex_clientid              |           | The trusted dex clientid                                                                       |
| metal_api_db_address                |           | The URL of the metal-db                                                                        |
| metal_api_db_password               |           | The password of the metal-db                                                                   |
| metal_api_ipam_grpc_server_endpoint |           | The grpc endpoint address of the ipam grpc service (requires scheme)                           |
| metal_api_nsq_lookupd_address       |           | The http address of nsqlookupd (only used for in-cluster traffic)                              |
| metal_api_nsq_tcp_address           |           | The tcp address of nsqd                                                                        |
| metal_api_nsq_http_address          |           | The http address of nsqd (only used for in-cluster traffic)                                    |
| metal_api_nsq_tls_enabled           |           | Enables TLS for nsq                                                                            |
| metal_api_nsq_tls_secret_name       |           | The name of the secret where nsq certificates are stored                                       |
| metal_api_nsq_tls_checksum          |           | The checksum of the nsq certificate data to imply a rolling update                             |
| metal_api_grpc_tls_enabled          |           | Enables TLS for gRPC                                                                           |
| metal_api_grpc_certs_ca_cert        |           | The gRPC ca certificate as a string                                                            |
| metal_api_grpc_certs_server_key     |           | The gRPC client key as a string                                                                |
| metal_api_grpc_certs_server_cert    |           | The gRPC client certificate as a string                                                        |
| metal_api_view_key                  |           | The HMAC view key of the metal-api used for API technical access                               |
| metal_api_edit_key                  |           | The HMAC edit key of the metal-api used for API technical access                               |
| metal_api_admin_key                 |           | The HMAC admin key of the metal-api used for API technical access                              |
| metal_api_sizes                     |           | Creates sizes (as masterdata) to the metal-api after deployment                                |
| metal_api_images                    |           | Creates images (as masterdata) to the metal-api after deployment                               |
| metal_api_partitions                |           | Creates partitions (as masterdata) to the metal-api after deployment                           |
| metal_api_networks                  |           | Creates networks (as masterdata) to the metal-api after deployment                             |
| metal_api_ips                       |           | Creates ips (as masterdata) to the metal-api after deployment                                  |
| metal_api_filesystemlayouts         |           | Creates filesystemlayouts to the metal-api after deployment                                    |
| metal_api_sizeimageconstraints      |           | Creates sizeimageconstraints to the metal-api after deployment                                 |
| metal_api_size_reservations         |           | Creates size reservations to the metal-api after deployment                                    |
| metal_api_resources                 |           | Sets the given container resources                                                             |
| metal_api_bmc_superuser_enabled     |           | Enables creating the BMC superuser and disabling the default one                               |
| metal_api_bmc_superuser_pwd         |           | If enabled use this password for the new BMC superuser                                         |
| metal_api_s3_enabled                |           | Whether the S3 server that serves firmware is enabled                                          |
| metal_api_s3_address                |           | The address of the S3 server that serves firmwares                                             |
| metal_api_s3_key                    |           | The key of the S3 server that serves firmwares                                                 |
| metal_api_s3_secret                 |           | The secret of the S3 server that serves firmwares                                              |
| metal_api_s3_firmware_bucket        |           | The S3 bucket name that contains the firmwares                                                 |
| metal_api_password_reason_minlength |           | If machine console password is requested this defines if and how long the given reason must be |
| metal_api_release_version           |           | The release version of metal-stack                                                             |
| minimum_client_version              |           | minimum metalctl version which is required to talk to this metal-api instance                  |

### metal-apiserver

| Name                                                                  | Mandatory | Description                                                               |
| --------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| metal_apiserver_enabled                                               |           | Enables the deployment of the metal-apiserver                             |
| metal_apiserver_replicas                                              |           | The number of deployed replicas of the metal-apiserver                    |
| metal_apiserver_db_addresses                                          |           | The addresses of the metal-db instances                                   |
| metal_apiserver_db_password                                           |           | The password of the metal-db                                              |
| metal_apiserver_redis_addr                                            |           | The address to a redis API                                                |
| metal_apiserver_redis_password                                        |           | The password to redis                                                     |
| metal_apiserver_oidc_discovery_url                                    |           | The URL for OIDC discovery                                                |
| metal_apiserver_oidc_end_session_url                                  |           | The URL for OIDC end session                                              |
| metal_apiserver_oidc_client_id                                        |           | The OIDC provider's app client id                                         |
| metal_apiserver_oidc_client_secret                                    |           | The OIDC provider's app client secret                                     |
| metal_apiserver_admin_subjects                                        |           | A list of token subjects that are allowed to create admin tokens          |
| metal_apiserver_session_secret                                        |           | The secret used to hash the sessions of a user during auth                |
| metal_apiserver_hpa_enabled:                                          |           | Enables horizontal pod autoscaling for the metal-apiserver                |
| metal_apiserver_hpa_max                                               |           | Max amount of replicas for the HPA of the metal-apiserver                 |
| metal_apiserver_hpa_min                                               |           | Min amount of replicas for the HPA of the metal-apiserver                 |
| metal_apiserver_hpa_cpu_percentage:                                   |           | Target CPU utilization percentage for the HPA of the metal-apiserver      |
| metal_apiserver_resources                                             |           | Sets the given container resources                                        |
| metal_apiserver_rate_limiting_max_requests_per_minute                 |           | The amount of requests allowed per minute for users with valid API tokens |
| metal_apiserver_rate_limiting_max_unauthenticated_requests_per_minute |           | The amount of requests allowed per minute for unauthenticated users       |

### masterdata-api

| Name                                 | Mandatory | Description                                                      |
|--------------------------------------|-----------|------------------------------------------------------------------|
| metal_masterdata_api_db_address      |           | The URL to the masterdata database                               |
| metal_masterdata_api_db_port         |           | The port of the masterdata database                              |
| metal_masterdata_api_db_name         |           | The database name of the masterdata database                     |
| metal_masterdata_api_db_user         |           | The user of the masterdata database                              |
| metal_masterdata_api_db_password     |           | The password of the masterdata database                          |
| metal_masterdata_api_provider_tenant |           | The name of the provider tenant                                  |
| metal_masterdata_api_tls_ca          | yes       | CA certificate key for the GRPC server                           |
| metal_masterdata_api_tls_cert        | yes       | Server certificate for the GRPC server                           |
| metal_masterdata_api_tls_cert_key    | yes       | Server certificate key for the GRPC server                       |
| metal_masterdata_api_tls_client_cert | yes       | Client certificate for the GRPC clients                          |
| metal_masterdata_api_tls_client_key  | yes       | Client certificate key for the GRPC clients                      |
| metal_masterdata_api_hmac            |           | The HMAC key of the masterdata-api used for API technical access |
| metal_masterdata_api_tenants         |           | Starts up the masterdata-api with given list of tenants          |
| metal_masterdata_api_projects        |           | Starts up the masterdata-api with the given list of projects     |
| metal_masterdata_api_resources       |           | Sets the given container resources                               |

### metal-console

| Name                                      | Mandatory | Description                                                        |
|-------------------------------------------|-----------|--------------------------------------------------------------------|
| metal_console_enabled                     |           | Whether to deploy or not to deploy the metal-console               |
| metal_console_replicas                    |           | The number of deployed replicas of the metal-console               |
| metal_console_resources                   |           | Sets the given container resources                                 |
| metal_console_bmc_proxy_certs_ca_cert     |           | The bmc-proxy ca certificate as a string (required if enabled)     |
| metal_console_bmc_proxy_certs_server_key  |           | The bmc-proxy server key as a string (required if enabled)         |
| metal_console_bmc_proxy_certs_server_pub  |           | The bmc-proxy server public key as a string (required if enabled)  |
| metal_console_bmc_proxy_certs_client_cert |           | The bmc-proxy client certificate as a string (required if enabled) |
| metal_console_bmc_proxy_certs_client_key  |           | The bmc-proxy client key as a string (required if enabled)         |

### ipam

| Name                   | Mandatory | Description                                                                       |
|------------------------|-----------|-----------------------------------------------------------------------------------|
| metal_ipam_db_address  |           | The hostname of the ipam service                                                  |
| metal_ipam_db_port     |           | The port of the ipam service                                                      |
| metal_ipam_db_name     |           | The database name of the ipam service                                             |
| metal_ipam_db_user     |           | The user of the ipam service                                                      |
| metal_ipam_db_password |           | The password of the ipam service                                                  |
| metal_ipam_log_level   |           | The log level for the ipam service (metal_log_level is not used for this service) |
| metal_ipam_resources   |           | Sets the given container resources                                                |

### Ingress

| Name                 | Mandatory | Description                                                                |
|----------------------|-----------|----------------------------------------------------------------------------|
| metal_deploy_ingress |           | Whether to deploy or not to deploy the ingress resource                    |
| metal_ingress        |           | Alternative configuration of the ingress (can be used for configuring TLS) |
| metal_ingress_dns    |           | The virtual host to reach the metal-api on                                 |

### Auditing

Configuration for metal-api:

| Name                                 | Mandatory | Description                                                                  |
| ------------------------------------ | --------- | ---------------------------------------------------------------------------- |
| metal_auditing_timescaledb_enabled   |           | Whether to deploy or not to configure timescaledb auditing. Default false.   |
| metal_auditing_timescaledb_host      |           | The timescaledb host                                                         |
| metal_auditing_timescaledb_port      |           | The timescaledb port                                                         |
| metal_auditing_timescaledb_db        |           | The timescaledb database name                                                |
| metal_auditing_timescaledb_user      |           | The timescaledb user                                                         |
| metal_auditing_timescaledb_password  |           | The timescaledb password                                                     |
| metal_auditing_timescaledb_retention |           | The timescaledb retention period, only configurable at first startup         |
| metal_auditing_search_backend        |           | Explicitly sets a configured audit backend to be used for search             |

Configuration for metal-apiserver:

| Name                                           | Mandatory | Description                                                               |
| ---------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| metal_apiserver_auditing_enabled               |           | Whether to deploy or not to configure timescaledb auditing. Default true. |
| metal_apiserver_auditing_timescaledb_host      |           | The timescaledb host                                                      |
| metal_apiserver_auditing_timescaledb_port      |           | The timescaledb port                                                      |
| metal_apiserver_auditing_timescaledb_db        |           | The timescaledb database name                                             |
| metal_apiserver_auditing_timescaledb_user      |           | The timescaledb user                                                      |
| metal_apiserver_auditing_timescaledb_password  |           | The timescaledb password                                                  |
| metal_apiserver_auditing_timescaledb_retention |           | The timescaledb retention period, only configurable at first startup      |
