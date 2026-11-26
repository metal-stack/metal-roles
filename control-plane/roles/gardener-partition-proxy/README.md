# gardener-partition-proxy

This role is intended to expose services through an [HAProxy](https://www.haproxy.org/) inside a Gardener shooted seed in order to make services from a partition accessible from the outside.

Requests are routed to the configured backends by the TLS SNI of the incoming connection. Clients always have to authenticate with a client certificate signed by the configured `ca` of the proxy server (mTLS). Every backend address is health checked and unhealthy addresses are taken out of the load balancing. By default, a TCP check (or TLS handshake for `https` and `grpcs` backends) is used. For `http` and `https` backends, an HTTP health check can be enabled by setting `health_check_path` for a proxy server.

Please note that this role creates `DNSRecord`s in the garden cluster's `garden` namespace.

## Examples

The following example deploys a proxy into the shooted seed `seed-a`, exposing two partition services:

- `duros` is a `grpcs` backend without an HTTP health check, so its addresses are only checked by a TLS handshake.
- `ontap` is an `https` backend with an HTTP health check, so its addresses are taken out of the load balancing when `GET /api/health` does not respond with a `2xx` or `3xx` status code.

```yaml
gardener_partition_proxy_shooted_seeds:
  - name: seed-a
    metal_project_id: 3e977e81-6ab5-4f28-b608-e7e94d62efb7
    metal_network_id: internet
    proxy_servers:
      - name: duros
        ingress_domain: duros.seed-a.proxy.example.com
        ca: "{{ duros_proxy_client_ca }}"
        cert: "{{ duros_proxy_cert }}"
        cert_key: "{{ duros_proxy_cert_key }}"
        addresses:
          - 10.0.0.10:443
          - 10.0.0.11:443
        type: grpcs
      - name: ontap
        ingress_domain: ontap.seed-a.proxy.example.com
        ca: "{{ ontap_proxy_client_ca }}"
        cert: "{{ ontap_proxy_cert }}"
        cert_key: "{{ ontap_proxy_cert_key }}"
        addresses:
          - 10.0.1.10:443
          - 10.0.1.11:443
        type: https
        health_check_path: /api/health
```

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# The admin token used to communicate with the metal-apiserver.
gardener_partition_proxy_deployment_admin_token: '{{ metal_deployment_admin_token | default(lookup(''env'', ''METAL_APIV2_TOKEN''), true) | default(None) }}'
# DNS credentials used for creating a DNS record for the proxy (base64 encoded secret data).
gardener_partition_proxy_dns_credentials: null
# The name of the DNS provider used for record creation.
gardener_partition_proxy_dns_provider: null
# The name of operator garden resource to derive the access kubeconfig for the virtual garden.
gardener_partition_proxy_garden_name: '{{ gardener_defaults_garden_name }}'
# The image name of the partition-proxy.
gardener_partition_proxy_image_name: haproxy
# The image tag of the partition-proxy.
gardener_partition_proxy_image_tag: 3.4-alpine
# The IP for the proxy. If not specified it will be automatically allocated in the metal-apiserver.
gardener_partition_proxy_ip_address: null
# The URL of the metal-apiserver used to allocate an IP address for the proxy in case a specific IP was not specified.
gardener_partition_proxy_metal_apiserver_url: '{{ metal_apiserver_url | default(lookup(''env'', ''METAL_APIV2_URL''), true) | default(None) }}'
# A list of shooted seeds in which to deploy a proxy.
gardener_partition_proxy_shooted_seeds: []
```
