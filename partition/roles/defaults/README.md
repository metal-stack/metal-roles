# defaults

Specifies common defaults for the metal-stack partition deployment.

## Variables


```yaml
# Default admin token for the metal API server.
defaults_partition_metal_apiserver_admin_token: '{{ metal_deployment_admin_token | default(lookup(''env'', ''METAL_APIV2_TOKEN''), true) | default(None) }}'
# Default URL for the metal API server.
defaults_partition_metal_apiserver_url: '{{ metal_apiserver_url | default(lookup(''env'', ''METAL_APIV2_URL''), true) | default(None) }}'
# ID of the partition.
metal_partition_id: null
# Address of the metal API.
metal_partition_metal_api_addr: null
# Base path of the metal API.
metal_partition_metal_api_basepath: /
# gRPC address of the metal API.
metal_partition_metal_api_grpc_address: '{{ metal_partition_metal_api_addr }}:50051'
# CA certificate for gRPC.
metal_partition_metal_api_grpc_ca_cert: null
# Directory for gRPC certificates.
metal_partition_metal_api_grpc_cert_dir: /certs/grpc
# Client certificate for gRPC.
metal_partition_metal_api_grpc_client_cert: null
# Client key for gRPC.
metal_partition_metal_api_grpc_client_key: null
# HMAC edit key for the metal API.
metal_partition_metal_api_hmac_edit_key: change-me
# HMAC view key for the metal API.
metal_partition_metal_api_hmac_view_key: change-me
# Port of the metal API.
metal_partition_metal_api_port: 443
# Protocol used by the metal API.
metal_partition_metal_api_protocol: https
# Management gateway for the partition.
metal_partition_mgmt_gateway: null
# Timezone for the partition.
metal_partition_timezone: null
```
