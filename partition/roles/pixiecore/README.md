# pixiecore

Deploys pixiecore in a systemd-managed Docker container.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../defaults/README.md).

```yaml
# Additional volumes to mount into the pixiecore container.
pixiecore_additional_volume_mounts: []
# REQUIRED: The host address on which the pixiecore API is reachable.
pixiecore_api_host: null
# The port on which the pixiecore API is served.
pixiecore_api_port: 4242
# Whether to enable debug logging.
pixiecore_debug: false
# DNS servers passed to the pixiecore container.
pixiecore_dns_servers: []
# Docker log driver for the pixiecore container.
pixiecore_docker_log_driver: json-file
# The address (host:port) of the metal-api gRPC server.
pixiecore_grpc_address: '{{ metal_partition_metal_api_grpc_address }}'
# The gRPC CA certificate content.
pixiecore_grpc_ca_cert: '{{ metal_partition_metal_api_grpc_ca_cert }}'
# Path to the gRPC certificate files on the host machine.
pixiecore_grpc_cert_dir: '{{ metal_partition_metal_api_grpc_cert_dir }}'
# The gRPC client certificate content.
pixiecore_grpc_client_cert: '{{ metal_partition_metal_api_grpc_client_cert }}'
# The gRPC client certificate key content.
pixiecore_grpc_client_key: '{{ metal_partition_metal_api_grpc_client_key }}'
# Image name of pixiecore. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
pixiecore_image_name: null
# Image tag of pixiecore. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
pixiecore_image_tag: null
# The metal-api view HMAC passed to metal-hammer.
pixiecore_metal_api_hmac_view_key: '{{ metal_partition_metal_api_hmac_view_key }}'
# The metal-api URL passed to metal-hammer.
pixiecore_metal_api_url: '{{ metal_partition_metal_api_protocol }}://{{ metal_partition_metal_api_addr }}:{{ metal_partition_metal_api_port }}{{ metal_partition_metal_api_basepath }}'
# Client certificate content for the metal-hammer logging endpoint.
pixiecore_metal_hammer_logging_cert: null
# Log forwarding endpoint for metal-hammer.
pixiecore_metal_hammer_logging_endpoint: null
# Client certificate key content for the metal-hammer logging endpoint.
pixiecore_metal_hammer_logging_key: null
# Basic auth password for the metal-hammer logging endpoint.
pixiecore_metal_hammer_logging_password: null
# Whether to skip TLS verification for the metal-hammer logging endpoint.
pixiecore_metal_hammer_logging_tls_insecure: false
# Basic auth user for the metal-hammer logging endpoint.
pixiecore_metal_hammer_logging_user: null
# NTP servers passed to metal-hammer.
pixiecore_metal_hammer_ntp_servers: []
# The partition id passed to pixiecore.
pixiecore_partition_id: '{{ metal_partition_id }}'
```
