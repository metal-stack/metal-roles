# metal

This role basically deploys the `metal-control-plane` [helm chart](https://github.com/metal-stack/helm-charts/tree/master/charts/metal-control-plane). It uses [hooks](https://github.com/helm/helm/blob/master/docs/charts_hooks.md) to deploy the control plane. There is a post-install hook to initialize the rethinkdb tables (there would be race conditions if there are multiple metal-api replicas initializing the database at the same time). Then, there are post-install and post-upgrade hooks to initialize and update the "masterdata" of the control plane (e.g. images, partitions, networks in this control plane).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# HMAC key for the metal-api admin access role.
metal_api_admin_key: change-me
# The base path of the metal-api.
metal_api_base_path: /metal/
# Whether the BMC superuser is enabled.
metal_api_bmc_superuser_enabled: false
# Password of the BMC superuser.
metal_api_bmc_superuser_pwd: change-me
# Address of the metal-db.
metal_api_db_address: metal-db
# Password of the metal-db.
metal_api_db_password: change-me
# The dex address used by the metal-api for OIDC.
metal_api_dex_address: ''
# The dex client id used by the metal-api for OIDC.
metal_api_dex_clientid: ''
# HMAC key for the metal-api edit access role.
metal_api_edit_key: change-me
# Filesystem layouts applied to the metal-api.
metal_api_filesystemlayouts: []
# REQUIRED: The metal-api gRPC CA certificate content.
metal_api_grpc_certs_ca_cert: null
# REQUIRED: The metal-api gRPC server certificate content.
metal_api_grpc_certs_server_cert: null
# REQUIRED: The metal-api gRPC server certificate key content.
metal_api_grpc_certs_server_key: null
# gRPC port of the metal-api.
metal_api_grpc_port: 50051
# Whether TLS is enabled for the metal-api gRPC server.
metal_api_grpc_tls_enabled: true
# The headscale API key used by the metal-api. Read from the headscale-api-key secret by default.
metal_api_headscale_api_key: '{{ lookup(''k8s'', api_version=''v1'', namespace=metal_control_plane_namespace, kind=''Secret'', resource_name=''headscale-api-key'').get(''data'', {}).get(''key'') | b64decode if metal_api_headscale_enabled else '''' }}'
# The external headscale control plane address used by the metal-api.
metal_api_headscale_control_plane_address: http{{ 's' if metal_api_headscale_tls }}://headscale.{{ metal_control_plane_gateway_dns }}
# Whether headscale VPN integration is enabled for the metal-api.
metal_api_headscale_enabled: false
# The internal headscale API address used by the metal-api.
metal_api_headscale_internal_api_address: headscale:50443
# Whether the headscale control plane address of the metal-api uses https.
metal_api_headscale_tls: true
# Target CPU utilization percentage of the metal-api HPA.
metal_api_hpa_cpu_percentage: 70
# Whether a horizontal pod autoscaler is deployed for the metal-api.
metal_api_hpa_enabled: false
# Maximum replicas of the metal-api HPA.
metal_api_hpa_max: 5
# Minimum replicas of the metal-api HPA.
metal_api_hpa_min: 3
# Whether to expose the metal-api through a GatewayAPI HTTPRoute instead of an ingress.
metal_api_httproute_enabled: false
# Hostnames for the metal-api HTTPRoute.
metal_api_httproute_hostnames:
- api.{{ metal_control_plane_gateway_dns }}
# HTTPS redirect configuration for the metal-api HTTPRoute.
metal_api_httproute_https_redirect: {}
# Parent references for the metal-api HTTPRoute.
metal_api_httproute_parent_refs: []
# Image name of the metal-api. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_api_image_name: null
# Image pull policy for the metal-api container.
metal_api_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the metal-api. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_api_image_tag: null
# Machine images applied to the metal-api.
metal_api_images: []
# Endpoint of the ipam gRPC server.
metal_api_ipam_grpc_server_endpoint: http://ipam:9090
# IPs applied to the metal-api.
metal_api_ips: []
# Metrics port of the metal-api.
metal_api_metrics_port: 2112
# Networks applied to the metal-api.
metal_api_networks: []
# The internal nsqd HTTP address.
metal_api_nsq_http_address: nsqd:4151
# The internal nsq-lookupd address.
metal_api_nsq_lookupd_address: nsq-lookupd:4161
# The external nsqd TCP address.
metal_api_nsq_tcp_address: '{{ metal_control_plane_gateway_dns }}:4150'
# Checksum over the nsqd TLS secret used to trigger pod restarts on certificate changes.
metal_api_nsq_tls_checksum: '{{ lookup(''k8s'', api_version=''v1'', namespace=metal_control_plane_namespace, kind=''Secret'', resource_name=''nsqd'').get(''data'', {}) | string | hash(''sha1'') if metal_api_nsq_tls_enabled else None }}'
# Whether TLS is used for the nsqd connection.
metal_api_nsq_tls_enabled: true
# Name of the secret containing the nsqd TLS certificates.
metal_api_nsq_tls_secret_name: nsqd
# Partitions applied to the metal-api.
metal_api_partitions: []
# Minimum length of the reason for requesting the machine console password.
metal_api_password_reason_minlength: null
# Whether a pod disruption budget is deployed for the metal-api.
metal_api_pdb_enabled: true
# Minimum available pods of the metal-api PDB.
metal_api_pdb_min_available: 2
# Service port of the metal-api.
metal_api_port: 8080
# The metal-stack release version reported by the metal-api.
metal_api_release_version: '{{ metal_stack_release_version }}'
# Amount of metal-api replicas.
metal_api_replicas: 3
# Resource requests and limits for the metal-api container.
metal_api_resources: null
# Address of the S3 endpoint for firmware. Required when metal_api_s3_enabled is true.
metal_api_s3_address: null
# Whether S3 is configured for serving firmware.
metal_api_s3_enabled: false
# S3 bucket containing the firmware.
metal_api_s3_firmware_bucket: null
# Access key of the S3 endpoint for firmware.
metal_api_s3_key: null
# Secret key of the S3 endpoint for firmware.
metal_api_s3_secret: null
# Size reservations applied to the metal-api.
metal_api_size_reservations: []
# Size image constraints applied to the metal-api.
metal_api_sizeimageconstraints: []
# Machine sizes applied to the metal-api.
metal_api_sizes: []
# Whether to expose the metal-api gRPC server through a GatewayAPI TCPRoute.
metal_api_tcproute_enabled: false
# Parent references for the metal-api TCPRoute.
metal_api_tcproute_parent_refs: []
# HMAC key for the metal-api view access role.
metal_api_view_key: change-me
# CA certificate for the splunk endpoint of metal-apiserver auditing.
metal_apiserver_auditing_splunk_ca: '{{ metal_auditing_splunk_ca }}'
# Whether auditing to splunk is enabled for the metal-apiserver.
metal_apiserver_auditing_splunk_enabled: '{{ metal_auditing_splunk_enabled }}'
# Splunk HEC endpoint for metal-apiserver auditing.
metal_apiserver_auditing_splunk_endpoint: '{{ metal_auditing_splunk_endpoint }}'
# Splunk HEC token for metal-apiserver auditing.
metal_apiserver_auditing_splunk_hec_token: '{{ metal_auditing_splunk_hec_token }}'
# Splunk host field for metal-apiserver auditing.
metal_apiserver_auditing_splunk_host: '{{ metal_auditing_splunk_host }}'
# Splunk index for metal-apiserver auditing.
metal_apiserver_auditing_splunk_index: '{{ metal_auditing_splunk_index }}'
# Splunk source for metal-apiserver auditing.
metal_apiserver_auditing_splunk_source: '{{ metal_auditing_splunk_source }}'
# Splunk source type for metal-apiserver auditing.
metal_apiserver_auditing_splunk_source_type: '{{ metal_auditing_splunk_source_type }}'
# Database name of the auditing timescaledb for the metal-apiserver.
metal_apiserver_auditing_timescaledb_db: '{{ metal_auditing_timescaledb_db }}'
# Whether auditing to timescaledb is enabled for the metal-apiserver.
metal_apiserver_auditing_timescaledb_enabled: '{{ metal_auditing_timescaledb_enabled }}'
# Host of the auditing timescaledb for the metal-apiserver.
metal_apiserver_auditing_timescaledb_host: '{{ metal_auditing_timescaledb_host }}'
# Password of the auditing timescaledb for the metal-apiserver.
metal_apiserver_auditing_timescaledb_password: '{{ metal_auditing_timescaledb_password }}'
# Port of the auditing timescaledb for the metal-apiserver.
metal_apiserver_auditing_timescaledb_port: '{{ metal_auditing_timescaledb_port }}'
# Retention period for audit traces of the metal-apiserver.
metal_apiserver_auditing_timescaledb_retention: '{{ metal_auditing_timescaledb_retention }}'
# User of the auditing timescaledb for the metal-apiserver.
metal_apiserver_auditing_timescaledb_user: '{{ metal_auditing_timescaledb_user }}'
# Addresses of the metal-db instances used by the metal-apiserver.
metal_apiserver_db_addresses:
- metal-db
# Password of the metal-db used by the metal-apiserver.
metal_apiserver_db_password: '{{ metal_api_db_password }}'
# Whether to deploy the metal-apiserver (v2 API).
metal_apiserver_enabled: true
# The headscale API key used by the metal-apiserver. Read from the headscale-api-key secret by default.
metal_apiserver_headscale_api_key: '{{ lookup(''k8s'', api_version=''v1'', namespace=metal_control_plane_namespace, kind=''Secret'', resource_name=''headscale-api-key'').get(''data'', {}).get(''key'') | b64decode if metal_apiserver_headscale_enabled else '''' }}'
# The external headscale control plane address used by the metal-apiserver.
metal_apiserver_headscale_control_plane_address: http{{ 's' if metal_apiserver_headscale_tls }}://headscale.{{ metal_control_plane_gateway_dns }}
# Whether headscale VPN integration is enabled for the metal-apiserver.
metal_apiserver_headscale_enabled: false
# The internal headscale API address used by the metal-apiserver.
metal_apiserver_headscale_internal_api_address: headscale:50443
# Whether the headscale control plane address of the metal-apiserver uses https.
metal_apiserver_headscale_tls: true
# Target CPU utilization percentage of the metal-apiserver HPA.
metal_apiserver_hpa_cpu_percentage: 70
# Whether a horizontal pod autoscaler is deployed for the metal-apiserver.
metal_apiserver_hpa_enabled: true
# Maximum replicas of the metal-apiserver HPA.
metal_apiserver_hpa_max: 5
# Minimum replicas of the metal-apiserver HPA.
metal_apiserver_hpa_min: 3
# Whether to expose the metal-apiserver through a GatewayAPI HTTPRoute instead of an ingress.
metal_apiserver_httproute_enabled: false
# Hostnames for the metal-apiserver HTTPRoute.
metal_apiserver_httproute_hostnames:
- v2.{{ metal_control_plane_gateway_dns }}
# HTTPS redirect configuration for the metal-apiserver HTTPRoute.
metal_apiserver_httproute_https_redirect: {}
# Parent references for the metal-apiserver HTTPRoute.
metal_apiserver_httproute_parent_refs: []
# Image name of the metal-apiserver. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_apiserver_image_name: null
# Image pull policy for the metal-apiserver container.
metal_apiserver_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the metal-apiserver. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_apiserver_image_tag: null
# OIDC client id for the metal-apiserver. Required when metal_apiserver_enabled is true. Read from the zitadel-client-credentials secret by default.
metal_apiserver_oidc_client_id: '{{ lookup(''k8s'', api_version=''v1'', namespace=metal_control_plane_namespace, kind=''Secret'', resource_name=''zitadel-client-credentials'').data.client_id | default('''') | b64decode }}'
# OIDC client secret for the metal-apiserver. Required when metal_apiserver_enabled is true. Read from the zitadel-client-credentials secret by default.
metal_apiserver_oidc_client_secret: '{{ lookup(''k8s'', api_version=''v1'', namespace=metal_control_plane_namespace, kind=''Secret'', resource_name=''zitadel-client-credentials'').data.client_secret | default('''') | b64decode }}'
# OIDC discovery URL for the metal-apiserver.
metal_apiserver_oidc_discovery_url: null
# OIDC end session URL for the metal-apiserver.
metal_apiserver_oidc_end_session_url: null
# Whether a pod disruption budget is deployed for the metal-apiserver.
metal_apiserver_pdb_enabled: true
# Minimum available pods of the metal-apiserver PDB.
metal_apiserver_pdb_min_available: 2
# Service port of the metal-apiserver.
metal_apiserver_port: 8080
# The provider tenant of the metal-apiserver.
metal_apiserver_provider_tenant: '{{ metal_control_plane_provider_tenant }}'
# Maximum authenticated requests per minute for the metal-apiserver.
metal_apiserver_rate_limiting_max_requests_per_minute: 1000
# Maximum unauthenticated requests per minute for the metal-apiserver.
metal_apiserver_rate_limiting_max_unauthenticated_requests_per_minute: 50
# Address of the redis/valkey instance used by the metal-apiserver.
metal_apiserver_redis_addr: valkey:6379
# Amount of metal-apiserver replicas.
metal_apiserver_replicas: 3
# Resource requests and limits for the metal-apiserver container.
metal_apiserver_resources: null
# Whether the metal-apiserver uses secure cookies.
metal_apiserver_secure_cookie: true
# Session secret of the metal-apiserver.
metal_apiserver_session_secret: null
# Whether the metal-apiserver skips TLS certificate verification.
metal_apiserver_tls_skip_verify: false
# Cron schedule for the metal-apiserver token creation job.
metal_apiserver_token_create_schedule: null
# Admin tokens created by the metal-apiserver token creation job.
metal_apiserver_tokens:
  admin_editor_token:
    tokenCreateRequest:
      adminRole: ADMIN_ROLE_EDITOR
      expires: 57600s
    user: '{{ metal_control_plane_provider_tenant }}'
  admin_viewer_token:
    tokenCreateRequest:
      adminRole: ADMIN_ROLE_VIEWER
      expires: 57600s
    user: '{{ metal_control_plane_provider_tenant }}'
# The external URL of the metal-apiserver.
metal_apiserver_url: https://v2.{{ metal_control_plane_gateway_dns }}
# The auditing backend used for searching audit traces.
metal_auditing_search_backend: null
# CA certificate for the splunk endpoint.
metal_auditing_splunk_ca: null
# Whether auditing to splunk is enabled.
metal_auditing_splunk_enabled: false
# Splunk HEC endpoint for auditing.
metal_auditing_splunk_endpoint: null
# Splunk HEC token for auditing.
metal_auditing_splunk_hec_token: null
# Splunk host field for auditing.
metal_auditing_splunk_host: null
# Splunk index for auditing.
metal_auditing_splunk_index: null
# Splunk source for auditing.
metal_auditing_splunk_source: null
# Splunk source type for auditing.
metal_auditing_splunk_source_type: null
# Database name of the auditing timescaledb.
metal_auditing_timescaledb_db: auditing
# Whether auditing to timescaledb is enabled.
metal_auditing_timescaledb_enabled: false
# Host of the auditing timescaledb.
metal_auditing_timescaledb_host: auditing-timescaledb
# Password of the auditing timescaledb.
metal_auditing_timescaledb_password: change-me
# Port of the auditing timescaledb.
metal_auditing_timescaledb_port: '5432'
# Retention period for audit traces.
metal_auditing_timescaledb_retention: 14 days
# User of the auditing timescaledb.
metal_auditing_timescaledb_user: postgres
# Whether to wait for the metal-api health endpoint after deployment.
metal_check_api_available: true
# The health endpoint URL that is probed after deployment.
metal_check_api_health_endpoint: https://{{ metal_api_ingress_dns }}{{ metal_api_base_path }}v1/health
# The metal-console BMC proxy CA certificate content.
metal_console_bmc_proxy_certs_ca_cert: null
# The metal-console BMC proxy client certificate content.
metal_console_bmc_proxy_certs_client_cert: null
# The metal-console BMC proxy client certificate key content.
metal_console_bmc_proxy_certs_client_key: null
# The metal-console BMC proxy server certificate key content.
metal_console_bmc_proxy_certs_server_key: null
# The metal-console BMC proxy server public key content.
metal_console_bmc_proxy_certs_server_pub: null
# Whether to deploy the metal-console.
metal_console_enabled: false
# Image name of the metal-console. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_console_image_name: null
# Image pull policy for the metal-console container.
metal_console_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the metal-console. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_console_image_tag: null
# Whether a pod disruption budget is deployed for the metal-console.
metal_console_pdb_enabled: false
# Minimum available pods of the metal-console PDB.
metal_console_pdb_min_available: 1
# Service port of the metal-console.
metal_console_port: 10001
# Amount of metal-console replicas.
metal_console_replicas: 3
# Resource requests and limits for the metal-console container.
metal_console_resources: null
# Whether to expose the metal-console through a GatewayAPI TCPRoute.
metal_console_tcproute_enabled: false
# Parent references for the metal-console TCPRoute.
metal_console_tcproute_parent_refs: []
# Whether to deploy the ingress resources.
metal_deploy_ingress: true
# Whether ingress rules for the v1 metal-api are rendered.
metal_deploy_ingress_api_v1_rules: '{{ True if not metal_api_httproute_enabled else False }}'
# Whether ingress rules for the v2 metal-apiserver are rendered.
metal_deploy_ingress_api_v2_rules: '{{ True if not metal_apiserver_httproute_enabled else False }}'
# OCI reference of the metal-control-plane helm chart. Required unless metal_helm_chart_local_path is set. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_helm_chart: null
# Local path to the metal-control-plane helm chart, used instead of the OCI chart when set.
metal_helm_chart_local_path: null
# Tag of the metal-control-plane helm chart. Required unless metal_helm_chart_local_path is set. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_helm_chart_tag: null
# Timeout for the helm deployment.
metal_helm_chart_timeout: 600s
# Version of the local metal-control-plane helm chart. Only evaluated when metal_helm_chart_local_path is set.
metal_helm_chart_version: null
# Additional ingress configuration (e.g. annotations).
metal_ingress: {}
# Ingress DNS name of the metal-api.
metal_ingress_dns: api.{{ metal_control_plane_ingress_dns | default(metal_control_plane_gateway_dns) }}
# Ingress DNS name of the metal-apiserver.
metal_ingress_v2_dns: v2.{{ metal_control_plane_ingress_dns | default(metal_control_plane_gateway_dns) }}
# Address of the ipam-db.
metal_ipam_db_address: ipam-db
# Database name of the ipam-db.
metal_ipam_db_name: ipam
# Password of the ipam-db.
metal_ipam_db_password: change-me
# Port of the ipam-db.
metal_ipam_db_port: 5432
# User of the ipam-db.
metal_ipam_db_user: postgres
# Image name of the ipam service. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_ipam_image_name: null
# Image pull policy for the ipam container.
metal_ipam_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the ipam service. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_ipam_image_tag: null
# Log level of the ipam service.
metal_ipam_log_level: debug
# Whether a pod disruption budget is deployed for the ipam service.
metal_ipam_pdb_enabled: true
# Minimum available pods of the ipam PDB.
metal_ipam_pdb_min_available: 1
# Resource requests and limits for the ipam container.
metal_ipam_resources: null
# Log level of the metal control plane components.
metal_log_level: info
# Address of the masterdata-db.
metal_masterdata_api_db_address: masterdata-db
# Database name of the masterdata-db.
metal_masterdata_api_db_name: masterdata
# Password of the masterdata-db.
metal_masterdata_api_db_password: change-me
# Port of the masterdata-db.
metal_masterdata_api_db_port: 5432
# User of the masterdata-db.
metal_masterdata_api_db_user: postgres
# HMAC key of the masterdata-api.
metal_masterdata_api_hmac: change-me
# Image name of the masterdata-api. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_masterdata_api_image_name: null
# Image pull policy for the masterdata-api container.
metal_masterdata_api_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the masterdata-api. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_masterdata_api_image_tag: null
# Metrics port of the masterdata-api.
metal_masterdata_api_metrics_port: 2113
# Whether a pod disruption budget is deployed for the masterdata-api.
metal_masterdata_api_pdb_enabled: true
# Minimum available pods of the masterdata-api PDB.
metal_masterdata_api_pdb_min_available: 1
# Service port of the masterdata-api.
metal_masterdata_api_port: 8443
# Projects applied to the masterdata-api.
metal_masterdata_api_projects: []
# The provider tenant of the masterdata-api.
metal_masterdata_api_provider_tenant: '{{ metal_control_plane_provider_tenant }}'
# Resource requests and limits for the masterdata-api container.
metal_masterdata_api_resources: null
# Tenants applied to the masterdata-api.
metal_masterdata_api_tenants: []
# REQUIRED: The masterdata-api CA certificate content.
metal_masterdata_api_tls_ca: null
# REQUIRED: The masterdata-api server certificate content.
metal_masterdata_api_tls_cert: null
# REQUIRED: The masterdata-api server certificate key content.
metal_masterdata_api_tls_cert_key: null
# REQUIRED: The masterdata-api client certificate content.
metal_masterdata_api_tls_client_cert: null
# REQUIRED: The masterdata-api client certificate key content.
metal_masterdata_api_tls_client_key: null
# Image name of metalctl. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_metalctl_image_name: null
# Image pull policy for the metalctl container.
metal_metalctl_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of metalctl. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_metalctl_image_tag: null
# Whether to set resource requests and limits on the control plane containers.
metal_set_resource_limits: true
# Address of the database used by the tenant-apiserver.
metal_tenant_apiserver_db_address: masterdata-db
# Database name used by the tenant-apiserver.
metal_tenant_apiserver_db_name: masterdata
# Database password used by the tenant-apiserver.
metal_tenant_apiserver_db_password: '{{ metal_masterdata_api_db_password | default(''change-me'', true) }}'
# Port of the database used by the tenant-apiserver.
metal_tenant_apiserver_db_port: 5432
# Database user used by the tenant-apiserver.
metal_tenant_apiserver_db_user: postgres
# Image name of the tenant-apiserver. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_tenant_apiserver_image_name: null
# Image pull policy for the tenant-apiserver container.
metal_tenant_apiserver_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of the tenant-apiserver. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
metal_tenant_apiserver_image_tag: null
# Whether a pod disruption budget is deployed for the tenant-apiserver.
metal_tenant_apiserver_pdb_enabled: true
# Minimum available pods of the tenant-apiserver PDB.
metal_tenant_apiserver_pdb_min_available: 1
# Amount of tenant-apiserver replicas.
metal_tenant_apiserver_replicas: 2
# Resource requests and limits for the tenant-apiserver container.
metal_tenant_apiserver_resources: null
# The minimum metalctl client version required by the metal-api.
minimum_client_version: '{{ metalctl_version }}'
```
