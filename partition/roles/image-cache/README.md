# image-cache

This role is being used to deploy an image cache to a partition.

The image-cache is highly-available and falls back to the "global image store" (the internet) on cache misses or cache backend issues.

For pointing your images to the image-cache, you use HTTP image URLs in the metal-api (the global image store will be accessed through HTTPS in case of a cache miss).

## Requirements

- The global images that you want to cache has to be hosted on S3-compatible cloud storage (this is the case for [images.metal-stack.io](https://images.metal-stack.io/), which is configured by default)

## Reasoning

Introducing a partition-local cache for machine images brings the following advantages:

- Significantly increase the download speed of OS images and hence shorten the time for provisioning new machines
- Independence from a global image store (the internet)
- Reduce load on the global image store

## Architecture

- The [metal-image-cache-sync](https://github.com/metal-stack/metal-image-cache-sync) service mirrors images from the global-image-store into the local file system, the partition-image-cache
- The DHCP server in the "bootstrap PXE network" tells PXE clients to use the management servers for DNS resolution
- CoreDNS is deployed on the management server and intercepts DNS requests that are directed to the global image store
  - This interception makes the image cache transparent for the clients
  - The global image store domain resolves to the IP of one of the management servers (round-robin)
- Haproxy is used to dispatch HTTP image downloads to the fastest available backends
  - If the image cache is running properly in the partition -> client downloads the image from there
    - Haproxy prefers the MinIO instance on the same server and load-balances between the other configured instances in case the local instance is down
    - If the image cache returns 404 not found on the requested image (cache sync), it redirects to the HTTPS frontend
    - The HTTPS frontend will just use forward to the global image store
  - If image-cache is not running on any of the management servers -> retrieve image from global image store
    - Haproxy will handle the SSL

## Variables

### Role Vars

| Name                                                        | Mandatory | Description                                                                                                               |
| ----------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| image_cache_global_image_stores                             |           | The image store addresses for which the DNS requests are intercepted and pointed to the image cache                       |
| image_cache_external_dns_servers                            |           | DNS servers that are used for resolving all other DNS requests                                                            |
| image_cache_coredns_image_name                              |           | The image name of CoreDNS                                                                                                 |
| image_cache_coredns_image_tag                               | yes       | The image tag of CoreDNS                                                                                                  |
| image_cache_sync_image_name                                 |           | The image name of metal-cache-image-sync                                                                                  |
| image_cache_sync_image_tag                                  | yes       | The image tag of metal-cache-image-sync                                                                                   |
| image_cache_sync_max_cache_size                             |           | Maximum size that the cache should have in the end (can exceed if min amount of images for all image variants is reached) |
| image_cache_sync_max_images_per_name                        |           | Maximum amount of images to cache for an image variant                                                                    |
| image_cache_sync_min_images_per_name                        |           | Minimum amount of images to keep of an image variant                                                                      |
| image_cache_sync_metal_api_endpoint                         | yes       | Endpoint of the metal-api                                                                                                 |
| image_cache_sync_metal_api_view_hmac                        | yes       | HMAC of the metal-api (requires view access)                                                                              |
| image_cache_sync_schedule                                   |           | Cron sync schedule                                                                                                        |
| image_cache_sync_excludes                                   |           | URL paths to exclude from the sync                                                                                        |
| image_cache_sync_host_path                                  |           | Root path of where to store the images                                                                                    |
| image_cache_sync_port                                       |           | The image tag of metal-cache-image-sync                                                                                   |
| image_cache_coredns_host_dir_path                           |           | The host path for CoreDNS configuration                                                                                   |
| image_cache_haproxy_image_name                              |           | The image name of haproxy                                                                                                 |
| image_cache_haproxy_image_tag                               | yes       | The image tag of haproxy                                                                                                  |
| image_cache_haproxy_host_dir_path                           |           | The host path for haproxy configuration                                                                                   |
| image_cache_haproxy_fallback_backend_server                 |           | The domain name of the "global image store" (internet, must have valid HTTPS)                                             |
| image_cache_haproxy_fallback_backend_server_health_endpoint |           | The health endpoint which is expected to return 200 of the "global image store"                                           |

### Host Vars

| Name                    | Mandatory | Description                                                                                                                            |
| ----------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| image_cache_internal_ip |           | Alternative IP (default is ansible_host) used for resolving DNS requests to image cache hosts and for internal component communication | 
