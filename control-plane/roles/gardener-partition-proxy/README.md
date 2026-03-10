# gardener-partition-proxy

This role is intended to expose services through an nginx proxy inside a Gardener shooted seed in order to make services from a partition accessible from the outside.

Please note that this role creates `DNSRecord`s in the garden cluster's `garden` namespace.

## Variables

| Name                                         | Mandatory | Description                                                                                  |
| -------------------------------------------- | --------- | -------------------------------------------------------------------------------------------- |
| gardener_partition_proxy_garden_name         |           | The name of operator garden resource to derive the access kubeconfig for the virtual garden  |
| gardener_partition_proxy_image_name          |           | The image name of the partition-proxy                                                        |
| gardener_partition_proxy_image_tag           |           | The image tag of the partition-proxy                                                         |
| gardener_partition_proxy_ip_address          |           | The IP for the proxy. If not specified it will be automatically allocated in the metal-api   |
| gardener_partition_proxy_metal_api_url       |           | The URL used to allocate an IP address for the proxy in case a specific IP was not specified |
| gardener_partition_proxy_metal_api_edit_hmac |           | The edit HMAC used to communicate with the metal-api                                         |
| gardener_partition_proxy_dns_credentials     |           | DNS credentials used for creating a DNS record for the proxy                                 |
| gardener_partition_proxy_dns_provider        |           | The name of the DNS provider used for record creation                                        |
| gardener_partition_proxy_shooted_seeds       |           | A list of shooted seeds in which to deploy a proxy                                           |
