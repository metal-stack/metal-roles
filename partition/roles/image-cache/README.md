# image-cache

This role is being used to deploy an image cache to a partition.

The image-cache is highly-available and falls back to the "global image store" (the internet) on cache misses or cache backend issues.

For pointing your images to the image cache, you are gonna use HTTP image URLs in the metal-api. CoreDNS will intercept HTTP image requests on port 80 and redirect them to the partition's image cache. The global image store will be accessed through HTTPS in case of a cache miss.

The cache is also capable of providing kernels and boot images configured in the metal-api.

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

- The [metal-image-cache-sync](https://github.com/metal-stack/metal-image-cache-sync) service mirrors images configured in the metal-api from the global-image-store into the local file system
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

### Role Vars

#### Images

| Name                           | Mandatory | Description                              |
| ------------------------------ | --------- | ---------------------------------------- |
| image_cache_sync_image_name    | yes       | The image name of metal-cache-image-sync |
| image_cache_sync_image_tag     | yes       | The image tag of metal-cache-image-sync  |
| image_cache_coredns_image_name | yes       | The image name of CoreDNS                |
| image_cache_coredns_image_tag  | yes       | The image tag of CoreDNS                 |
| image_cache_haproxy_image_name | yes       | The image name of haproxy                |
| image_cache_haproxy_image_tag  | yes       | The image tag of haproxy                 |

#### Configuration

| Name                                                                   | Mandatory | Description                                                                                                               |
| ---------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| image_cache_intercept_domains                                          |           | The domains for which the DNS requests are intercepted and pointed to the image cache                                     |
| image_cache_kernel_cache_enabled                                       |           | Enables caching partition boot kernels                                                                                    |
| image_cache_boot_image_cache_enabled                                   |           | Enables caching partition boot images                                                                                     |
| image_cache_external_dns_servers                                       |           | DNS servers that are used for resolving all other DNS requests                                                            |
| image_cache_sync_max_cache_size                                        |           | Maximum size that the cache should have in the end (can exceed if min amount of images for all image variants is reached) |
| image_cache_sync_expiration_grace_period                               |           | The amount of days to still sync images even if they have already expired in the metal-api                                |
| image_cache_sync_max_images_per_name                                   |           | Maximum amount of images to cache for an image variant                                                                    |
| image_cache_sync_min_images_per_name                                   |           | Minimum amount of images to keep of an image variant                                                                      |
| image_cache_sync_metal_api_endpoint                                    | yes       | Endpoint of the metal-api                                                                                                 |
| image_cache_sync_metal_api_view_hmac                                   | yes       | HMAC of the metal-api (requires view access)                                                                              |
| image_cache_sync_schedule                                              |           | Cron sync schedule                                                                                                        |
| image_cache_sync_excludes                                              |           | URL paths to exclude from the sync                                                                                        |
| image_cache_sync_host_path                                             |           | Root path of where to store the images                                                                                    |
| image_cache_sync_port                                                  |           | The image tag of metal-cache-image-sync                                                                                   |
| image_cache_coredns_host_dir_path                                      |           | The host path for CoreDNS configuration                                                                                   |
| image_cache_kernel_route_prefix                                        |           | The route prefix to distinguish whether the kernel cache backend is used or not                                           |
| image_cache_boot_image_route_prefix                                    |           | The route prefix to distinguish whether the boot image cache backend is used or not                                       |
| image_cache_haproxy_host_dir_path                                      |           | The host path for haproxy configuration                                                                                   |
| image_cache_haproxy_fallback_backend_server                            |           | The domain name of the "global image store" (internet, must have valid HTTPS)                                             |
| image_cache_haproxy_fallback_backend_server_health_endpoint            |           | The health endpoint which is expected to return 200 of the "global image store"                                           |
| image_cache_haproxy_kernel_fallback_backend_server                     |           | The domain name of the "global kernel store" (internet, must have valid HTTPS)                                            |
| image_cache_haproxy_kernel_fallback_backend_server_health_endpoint     |           | The health endpoint which is expected to return 200 of the "global kernel store"                                          |
| image_cache_haproxy_boot_image_fallback_backend_server                 |           | The domain name of the "global boot image store" (internet, must have valid HTTPS)                                        |
| image_cache_haproxy_boot_image_fallback_backend_server_health_endpoint |           | The health endpoint which is expected to return 200 of the "global boot image store"                                      |

### Host Vars

| Name                    | Mandatory | Description                                                                                                                            |
| ----------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| image_cache_internal_ip |           | Alternative IP (default is ansible_host) used for resolving DNS requests to image cache hosts and for internal component communication |
