# gardener-partition-proxy

This role is intended to expose services through an nginx proxy inside a Gardener shooted seed in order to make services from a partition accessible from the outside.

Please note that this role creates `DNSRecord`s in the garden cluster's `garden` namespace.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# Credentials for the DNS provider of the proxy DNS entry.
gardener_partition_proxy_dns_credentials: null
# The DNS provider type of the proxy DNS entry.
gardener_partition_proxy_dns_provider: null
# Name of the garden.
gardener_partition_proxy_garden_name: '{{ gardener_defaults_garden_name }}'
# Image name of the proxy.
gardener_partition_proxy_image_name: nginx
# Image tag of the proxy.
gardener_partition_proxy_image_tag: 1.31-alpine
# The load balancer IP address of the proxy service.
gardener_partition_proxy_ip_address: null
# The metal-api edit HMAC used for looking up partitions.
gardener_partition_proxy_metal_api_edit_hmac: null
# The metal-api URL that the proxy forwards to.
gardener_partition_proxy_metal_api_url: null
# The shooted seeds to deploy the proxy to.
gardener_partition_proxy_shooted_seeds: []
```
