# metal

This role contains a [helm chart](control-plane/metal/files/metal-control-plane) that contains all major components to run the Metal Stack. If you do not want to use Ansible for deployment, this chart can be the starting point for your deployment of Metal Stack.

The helm chart uses [hooks](https://github.com/helm/helm/blob/master/docs/charts_hooks.md) to deploy the control plane. There is a post-install hook to initialize the rethinkdb tables (there would be race conditions if there are multiple metal-api replicas initializing the database at the same time). Then, there are post-install and post-upgrade hooks to initialize and update the "masterdata" of the control plane (e.g. images, partitions, networks in this control plane).

As our control plane also requires non-HTTP ports to be exposed to the outside world, we currently use [tcp and udp service exposal of Kubernetes nginx-ingress](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

### General

| Name                               | Mandatory | Description                                                                                                                        |
| ---------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| metal_expose_ingress_service_ports |           | Exposes tcp and udp services over nginx-ingress, requires [nginx-ingress](https://github.com/kubernetes/ingress-nginx) to be setup |
| metal_check_api_available          |           | Checks whether the metal-api is reachable from the outside after deployment                                                        |
| metal_check_api_health_endpoint    |           | The endpoint to call if the metal-api is reachable from the outside after deployment                                               |
| metal_set_resource_limits          |           | Deploys metal components with or without resource limits (possibly disable for development environments)                           |
| metal_log_level                    |           | The log level of the control plane components                                                                                      |
| metal_log_encoding                 |           | The output format of the logger                                                                                                    |

### Images

**You may pin all images to specific versions and not to `latest`.**

| Name                      | Mandatory | Description                         |
| ------------------------- | --------- | ----------------------------------- |
| metal_api_image_name      |           | Image version of the metal-api      |
| metal_api_image_tag       |           | Image tag of the metal-api          |
| metalctl_image_name       |           | Image version of the metalctl       |
| metalctl_image_tag        |           | Image tag of the metalctl           |
| metal_console_image_name  |           | Image version of the metal-console  |
| metal_console_image_tag   |           | Image tag of the metal-console      |
| masterdata_api_image_name |           | Image version of the masterdata-api |
| masterdata_api_image_tag  |           | Image tag of the masterdata-api     |

### metal-api

| Name                          | Mandatory | Description                                                          |
| ----------------------------- | --------- | -------------------------------------------------------------------- |
| metal_api_replicas            |           | The number of deployed replicas of the metal-api                     |
| metal_api_base_path           |           | The base path of the HTTP server                                     |
| metal_api_dex_address         |           | The URL to the dex server                                            |
| metal_api_db_address          |           | The URL of the metal-db                                              |
| metal_api_db_password         |           | The password of the metal-db                                         |
| metal_api_ipam_db_address     |           | The URL to the ipam database                                         |
| metal_api_ipam_db_port        |           | The port of the ipam database                                        |
| metal_api_ipam_db_name        |           | The database name of the ipam database                               |
| metal_api_ipam_db_user        |           | The user of the ipam database                                        |
| metal_api_ipam_db_password    |           | The password of the ipam database                                    |
| metal_api_nsq_tcp_address     |           | The tcp address of nsqd                                              |
| metal_api_nsq_http_address    |           | The http address of nsqd (only used for in-cluster traffic)          |
| metal_api_nsq_tls_enabled     |           | Enables TLS for nsq                                                  |
| metal_api_nsq_tls_secret_name |           | The name of the secret where nsq certificates are stored             |
| metal_api_view_key            |           | The HMAC view key of the metal-api used for API technical access     |
| metal_api_edit_key            |           | The HMAC edit key of the metal-api used for API technical access     |
| metal_api_admin_key           |           | The HMAC admin key of the metal-api used for API technical access    |
| metal_api_sizes               |           | Creates sizes (as masterdata) to the metal-api after deployment      |
| metal_api_images              |           | Creates images (as masterdata) to the metal-api after deployment     |
| metal_api_partitions          |           | Creates partitions (as masterdata) to the metal-api after deployment |
| metal_api_networks            |           | Creates networks (as masterdata) to the metal-api after deployment   |
| metal_api_ips                 |           | Creates ips (as masterdata) to the metal-api after deployment        |

### masterdata-api

| Name                                 | Mandatory | Description                                                      |
| ------------------------------------ | --------- | ---------------------------------------------------------------- |
| metal_masterdata_api_db_address      |           | The URL to the masterdata database                               |
| metal_masterdata_api_db_port         |           | The port of the masterdata database                              |
| metal_masterdata_api_db_name         |           | The database name of the masterdata database                     |
| metal_masterdata_api_db_user         |           | The user of the masterdata database                              |
| metal_masterdata_api_db_password     |           | The password of the masterdata database                          |
| metal_masterdata_api_provider_tenant |           | The name of the provider tenant                                  |
| metal_masterdata_api_tls_server_key  |           | Server certificate key for the GRPC server                       |
| metal_masterdata_api_tls_server_cert |           | Server certificate for the GRPC server                           |
| metal_masterdata_api_hmac            |           | The HMAC key of the masterdata-api used for API technical access |
| metal_masterdata_api_tenants         |           | Starts up the masterdata-api with given list of tenants          |
| metal_masterdata_api_projects        |           | Starts up the masterdata-api with the given list of projects     |

# metal-console

| Name                   | Mandatory | Description                                                                                                 |
| ---------------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| metal_console_replicas |           | The number of deployed replicas of the metal-console                                                        |
| metal_mgmt_services    |           | Endpoints to reverse bmc-proxies located inside the partitions for establishing machine console connections |

# Ingress

| Name                 | Mandatory | Description                                                                |
| -------------------- | --------- | -------------------------------------------------------------------------- |
| metal_deploy_ingress |           | Whether to deploy or not to deploy the ingress resource                    |
| metal_ingress        |           | Alternative configuration of the ingress (can be used for configuring TLS) |
| metal_ingress_dns    |           | The virtual host to reach the metal-api on                                 |
