# image-cache

This role is being used to deploy an image cache to a partition.

The image-cache is highly-available and falls back to the "global image store" (the internet) on cache misses or cache backend issues.

For pointing your images to the image cache, you are gonna use HTTP image URLs in the metal-apiserver. CoreDNS will intercept HTTP image requests on port 80 and redirect them to the partition's image cache. The global image store will be accessed through HTTPS in case of a cache miss.

The cache is also capable of providing kernels and boot images configured in the metal-apiserver.

## Requirements

- Your DHCP inside your partition's PXE boot network needs to point the machines to the image cache servers for their DNS resolution
- The global images that you want to cache have to be hosted on S3-compatible cloud storage (this is the case for our official image store [images.metal-stack.io](https://images.metal-stack.io/), which you are free to use and is configured by default)
- The global image store requires a valid HTTPS certificate (in case you use your own image store)

## Reasoning

Introducing a partition-local cache for machine images brings the following advantages:

- Significantly increase the download speed of OS images and hence shorten the time for provisioning new machines
- Independence from a global image store (the internet)
- Reduce load on the global image store

## Architecture

- The [metal-image-cache-sync](https://github.com/metal-stack/metal-image-cache-sync) service mirrors images configured in the metal-apiserver from the global-image-store into the local file system
- CoreDNS is deployed on the management server and intercepts DNS requests that are directed to the global image store
  - This approach makes the image cache transparent for the clients
  - The global image store domain resolves to the IP of one of the image cache servers (round-robin)
- Haproxy is used to dispatch HTTP image downloads to the fastest available backends
  - If the image cache is running properly in the partition -> client downloads the image from there
    - Haproxy prefers the image cache on the same server and load-balances between the other configured instances in case the local instance is down
    - If the image cache does not find the requested resource, the cache returns a 307 redirect (cache miss), the requester will now attempt to access the same resource via HTTPS
    - The HTTPS frontend forwards the request to the global image store (client does SSL)
  - If the image cache is not running on any of the servers -> retrieve image from global image store
    - Haproxy will handle the SSL

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/partition/roles/defaults](../defaults/README.md).

```yaml
# The hosts serving as image cache backends.
image_cache_backend_hosts: '{{ play_hosts }}'
# Whether to cache metal-hammer boot images.
image_cache_boot_image_cache_enabled: true
# HTTP route prefix under which cached boot images are served.
image_cache_boot_image_route_prefix: /metal-stack/metal-hammer
# Docker log driver for the CoreDNS container.
image_cache_coredns_docker_log_driver: json-file
# Host directory for the CoreDNS configuration.
image_cache_coredns_host_dir_path: /coredns
# Image name of CoreDNS. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_coredns_image_name: null
# Image tag of CoreDNS. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_coredns_image_tag: null
# External DNS servers (name, ip) used for forwarding non-intercepted DNS requests.
image_cache_external_dns_servers:
- ip: 8.8.8.8
  name: google
- ip: 1.1.1.1
  name: cloudflare01
- ip: 1.0.0.1
  name: cloudflare02
# Fallback backend server for boot images.
image_cache_haproxy_boot_image_fallback_backend_server: github.com
# Health check endpoint of the boot image fallback backend server.
image_cache_haproxy_boot_image_fallback_backend_server_health_endpoint: /
# Docker log driver for the haproxy container.
image_cache_haproxy_docker_log_driver: json-file
# Fallback backend server (must be reachable over https with a valid certificate) used when the local image cache is unavailable.
image_cache_haproxy_fallback_backend_server: images.metal-stack.io
# Health check endpoint of the fallback backend server.
image_cache_haproxy_fallback_backend_server_health_endpoint: /
# Host directory for the haproxy configuration.
image_cache_haproxy_host_dir_path: /haproxy
# Image name of haproxy. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_haproxy_image_name: null
# Image tag of haproxy. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_haproxy_image_tag: null
# Fallback backend server for kernels.
image_cache_haproxy_kernel_fallback_backend_server: github.com
# Health check endpoint of the kernel fallback backend server.
image_cache_haproxy_kernel_fallback_backend_server_health_endpoint: /
# Domains for which DNS requests are intercepted and resolved to the image cache.
image_cache_intercept_domains:
- images.metal-stack.io
- github.com
# Alternative IP (default is ansible_host) used for resolving DNS requests to image cache hosts and for internal component communication.
image_cache_internal_ip: null
# Whether to cache metal-hammer kernels.
image_cache_kernel_cache_enabled: true
# HTTP route prefix under which cached kernels are served.
image_cache_kernel_route_prefix: /metal-stack/kernel
# Port on which cached boot images are served.
image_cache_sync_boot_image_port: 9003
# Docker log driver for the image sync container.
image_cache_sync_docker_log_driver: json-file
# Image path substrings excluded from syncing.
image_cache_sync_excludes:
- /pull_requests/
# Grace period for expired images before removal from the cache.
image_cache_sync_expiration_grace_period: 0
# Host path where synced images are stored.
image_cache_sync_host_path: /metal-image-cache-sync
# Image name of metal-image-cache-sync. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_sync_image_name: null
# Image tag of metal-image-cache-sync. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
image_cache_sync_image_tag: null
# Port on which cached kernels are served.
image_cache_sync_kernel_port: 9002
# Maximum size of the image cache (e.g. 100G).
image_cache_sync_max_cache_size: 100G
# Maximum amount of images to keep per image name (-1 for unlimited).
image_cache_sync_max_images_per_name: -1
# The metal-api endpoint used for looking up images to sync.
image_cache_sync_metal_api_endpoint: null
# REQUIRED: The metal-api view HMAC used for authenticating against the metal-api.
image_cache_sync_metal_api_view_hmac: null
# Minimum amount of images to keep per image name.
image_cache_sync_min_images_per_name: 4
# Port on which cached OS images are served.
image_cache_sync_port: 9001
# Cron schedule for the image sync.
image_cache_sync_schedule: '*/10 * * * *'
```
