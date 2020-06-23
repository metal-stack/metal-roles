# image-cache

This role is being used to deploy an image cache to a partition.

The image-cache is highly-available and falls back to the "global image store" (the internet) on cache misses or cache backend issues.

For pointing your images to the image-cache, you use an HTTP URL to the image (the global image store will be accessed through HTTPS in case of a cache miss).

## Requirements

- **The global images that you want to cache have to be hosted on GKE** (this is the case for [images.metal-stack.io](https://images.metal-stack.io/))
- `mgmt_servers` group in the inventory grouping the managements servers
- `switch_mgmt_ip` variable in the inventory hostvars for a management server
- [MinIO Client](https://docs.min.io/docs/minio-client-complete-guide.html) as part of the deployment base image

## Reasoning

Introducing a partition-local cache for machine images brings the following advantages:

- Significantly increase the download speed of OS images and hence shorten the time for provisioning new machines
- Independence from a global image store (the internet)
- Reduce load on the global image store

## Architecture

- MinIO is deployed on the management servers, this is the actual cache
- Image-Sync is a small service to mirror images from the global-image-store into the partition-image-cache
- The DHCP server in the "bootstrap PXE network" tells PXE clients to use the management servers for DNS resolution
- CoreDNS is deployed on the management server and intercepts DNS requests that are directed to the global image store
  - This interception makes the image cache transparent for the clients
  - The global image store domain resolves to the IP of one of the management servers (round-robin)
- Haproxy is used to dispatch HTTP image downloads to the fastest available backends
  - If MinIO is running properly in the partition -> client downloads the image from MinIO
    - Haproxy prefers the MinIO instance on the same server and load-balances between the other configured instances in case the local instance is down
    - If MinIO returns 404 not found on the image (which can happen when images are not yet synced), it redirects to the HTTPS frontend
    - The HTTPS frontend will just use forward to the global image store
  - If MinIO is not running on any of the management servers -> retrieve image from global image store
    - Haproxy will handle the SSL

## Variables

| Name                                                        | Mandatory | Description                                                                                         |
| ----------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------- |
| image_cache_global_image_stores                             |           | The image store addresses for which the DNS requests are intercepted and pointed to the image cache |
| image_cache_external_dns_servers                            |           | DNS servers that are used for resolving all other DNS requests                                      |
| image_cache_coredns_image_name                              |           | The image name of CoreDNS                                                                           |
| image_cache_coredns_image_tag                               |           | The image tag of CoreDNS                                                                            |
| image_cache_coredns_host_dir_path                           |           | The host path for CoreDNS configuration                                                             |
| image_cache_haproxy_image_name                              |           | The image name of haproxy                                                                           |
| image_cache_haproxy_image_tag                               |           | The image tag of haproxy                                                                            |
| image_cache_haproxy_host_dir_path                           |           | The host path for haproxy configuration                                                             |
| image_cache_haproxy_fallback_backend_server                 |           | The domain name of the "global image store" (internet, must have valid HTTPS)                       |
| image_cache_haproxy_fallback_backend_server_health_endpoint |           | The health endpoint which is expected to return 200 of the "global image store"                     |
| image_cache_minio_image_name                                |           | The image name of Minio                                                                             |
| image_cache_minio_image_tag                                 |           | The image tag of Minio                                                                              |
| image_cache_minio_port                                      |           | The port Minio listens on                                                                           |
| image_cache_minio_host_dir_path                             |           | The host path for Minio configuration                                                               |
| image_cache_minio_data_host_dir                             |           | The host path for Minio to store the images in                                                      |
| image_cache_imagesync_image_name                            |           | The image name of image-sync                                                                        |
| image_cache_imagesync_image_tag                             |           | The image tag of image-sync                                                                         |
| image_cache_imagesync_src                                   |           | The source bucket path to mirror images from                                                        |
| image_cache_imagesync_dest                                  |           | The destination path where the mirrored images are put                                              |
| image_cache_imagesync_interval_sec                          |           | The interval in which images will be synced                                                         |
