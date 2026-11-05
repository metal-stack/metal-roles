# isolated clusters

Contains roles for deploying additional services for the isolated cluster feature as described [here](https://docs.metal-stack.io/stable/overview/isolated-kubernetes/).

It contains the services:

- oci-mirror
- Registry
- DNS
- NTP
- Ingress Controller (nginx-ingress)
- Envoy Gateway (optional, alternative to nginx-ingress)

A cert-manager is expected to be deployed by the user beforehand.

## Ingress vs Envoy Gateway

This role supports two options for exposing services:

1. **nginx-ingress** (default, enabled by default): Traditional Ingress controller for HTTP/HTTPS traffic and TCP/UDP proxying
2. **Envoy Gateway** (optional): Modern Gateway API implementation supporting HTTP/HTTPS, TCP, and UDP protocols

You can enable/disable each option independently using the `isolated_clusters_ingress_controller_enabled` and `isolated_clusters_envoy_gateway_enabled` variables. Both can be enabled simultaneously if needed.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Image name of the CoreDNS DNS service.
isolated_clusters_dns_image_name: coredns/coredns
# REQUIRED: Image tag of the CoreDNS DNS service.
isolated_clusters_dns_image_tag: null
# The namespace to deploy the DNS service to.
isolated_clusters_dns_namespace: dns-service
# Version of the envoy gateway helm chart. Required when the envoy gateway is enabled.
isolated_clusters_envoy_gateway_chart_version: null
# Whether to deploy the envoy gateway.
isolated_clusters_envoy_gateway_enabled: false
# Load balancer IP of the envoy gateway service.
isolated_clusters_envoy_gateway_load_balancer_ip: null
# Load balancer source ranges of the envoy gateway service.
isolated_clusters_envoy_gateway_load_balancer_source_ranges: null
# The namespace to deploy the envoy gateway to.
isolated_clusters_envoy_gateway_namespace: envoy-gateway-system
# Name of the TLS secret used for the registry route of the envoy gateway.
isolated_clusters_envoy_gateway_registry_tls_secret_name: registry-tls-cert
# Amount of envoy gateway replicas.
isolated_clusters_envoy_gateway_replicas: 1
# UDP session idle timeout of the envoy gateway.
isolated_clusters_envoy_gateway_udp_session_idle_timeout: 1s
# Label value used for grouping the isolated cluster services.
isolated_clusters_group_label: '{{ metal_control_plane_stage_name }}'
# Version of the ingress-nginx helm chart. Required when the ingress controller is enabled.
isolated_clusters_ingress_controller_chart_version: null
# Whether the ingress controller runs in a chroot.
isolated_clusters_ingress_controller_chroot: true
# Whether to deploy the ingress controller.
isolated_clusters_ingress_controller_enabled: true
# Load balancer IP of the ingress controller service. Required when the ingress controller is enabled.
isolated_clusters_ingress_controller_load_balancer_ip: null
# Load balancer source ranges of the ingress controller service. Required when the ingress controller is enabled.
isolated_clusters_ingress_controller_load_balancer_source_ranges: null
# The namespace to deploy the ingress controller to.
isolated_clusters_ingress_controller_namespace: ingress
# Amount of ingress controller replicas.
isolated_clusters_ingress_controller_replicas: null
# Image name of the chrony NTP service.
isolated_clusters_ntp_image_name: ghcr.io/metal-stack/chrony
# REQUIRED: Image tag of the chrony NTP service.
isolated_clusters_ntp_image_tag: null
# The namespace to deploy the NTP service to.
isolated_clusters_ntp_namespace: ntp-service
# The clusters to install the partition services into.
isolated_clusters_partition_services_cluster: []
# FQDN under which the registry is reachable through the envoy gateway. Required when the envoy gateway is enabled.
isolated_clusters_registry_fqdn: null
# Image name of the registry.
isolated_clusters_registry_image_name: docker.io/registry
# REQUIRED: Image tag of the registry.
isolated_clusters_registry_image_tag: null
# Additional annotations for the registry ingress.
isolated_clusters_registry_ingress_annotations: {}
# FQDN under which the registry is reachable through the ingress controller. Required when the ingress controller is enabled.
isolated_clusters_registry_ingress_fqdn: null
# The namespace to deploy the registry to.
isolated_clusters_registry_namespace: registry
# Configuration of the oci-mirror (registries and images to mirror).
isolated_clusters_registry_oci_mirror_config:
  images:
  - destination: http://registry:5000/fluent/fluentd
    match:
      semver: '>= v1.12'
    source: docker.io/fluent/fluentd
  - destination: http://registry:5000/calico/cni
    match:
      semver: '>= v3.29.7'
    source: quay.io/calico/cni
  - destination: http://registry:5000/calico/node
    match:
      semver: '>= v3.29.7'
    source: quay.io/calico/node
  - destination: http://registry:5000/lightos-csi/lb-csi-plugin
    match:
      semver: '>= 1.21.0'
    source: docker.lightbitslabs.com/lightos-csi/lb-csi-plugin
  - destination: http://registry:5000/lightos-csi/lb-nvme-discovery-client
    match:
      semver: '>= 1.21.0'
    source: docker.lightbitslabs.com/lightos-csi/lb-nvme-discovery-client
  - destination: http://registry:5000/gardener-project/releases/hyperkube
    match:
      semver: '>= v1.29.0'
    source: europe-docker.pkg.dev/gardener-project/releases/hyperkube
  - destination: http://registry:5000/gardener-project/releases/gardener/node-agent
    match:
      semver: '>= v1.128.7'
    source: europe-docker.pkg.dev/gardener-project/releases/gardener/node-agent
  - destination: http://registry:5000/gardener-project/releases/gardener/vpn-client
    match:
      semver: '>= 0.42.0'
    source: europe-docker.pkg.dev/gardener-project/releases/gardener/vpn-client
  - destination: http://registry:5000/gardener-project/releases/3rd/alpine
    match:
      semver: '>= 3.22.1'
    source: europe-docker.pkg.dev/gardener-project/releases/3rd/alpine
  - destination: http://registry:5000/gardener-project/releases/gardener/alpine-conntrack
    match:
      semver: '>= 3.21.3'
    source: europe-docker.pkg.dev/gardener-project/releases/gardener/alpine-conntrack
  - destination: http://registry:5000/gardener-project/releases/3rd/envoyproxy/envoy
    match:
      all_tags: true
    source: europe-docker.pkg.dev/gardener-project/releases/3rd/envoyproxy/envoy
  - destination: http://registry:5000/gardener-project/releases/gardener/apiserver-proxy
    match:
      semver: '>= v0.19.0'
    source: europe-docker.pkg.dev/gardener-project/releases/gardener/apiserver-proxy
  - destination: http://registry:5000/metal-stack/metallb-health-sidecar
    match:
      semver: '>= v0.1.2'
    source: ghcr.io/metal-stack/metallb-health-sidecar
  - destination: http://registry:5000/metal-stack/csi-driver-lvm
    match:
      semver: '>= v0.8.2'
    source: ghcr.io/metal-stack/csi-driver-lvm
  - destination: http://registry:5000/metal-stack/csi-driver-lvm-provisioner
    match:
      semver: '>= v0.8.2'
    source: ghcr.io/metal-stack/csi-driver-lvm-provisioner
  - destination: http://registry:5000/metal-stack/csi-driver-lvm-controller
    match:
      semver: '>= v0.8.2'
    source: ghcr.io/metal-stack/csi-driver-lvm-controller
  - destination: http://registry:5000/metallb/controller
    match:
      semver: '>= v0.15.2'
    source: quay.io/metallb/controller
  - destination: http://registry:5000/metallb/speaker
    match:
      semver: '>= v0.15.2'
    source: quay.io/metallb/speaker
  - destination: http://registry:5000/prometheus/blackbox-exporter
    match:
      semver: '>= v0.26.0'
    source: quay.io/prometheus/blackbox-exporter
  - destination: http://registry:5000/prometheus/node-exporter
    match:
      semver: '>= v1.9.1'
    source: quay.io/prometheus/node-exporter
  - destination: http://registry:5000/pause
    match:
      semver: '>= 3.8'
    source: registry.k8s.io/pause
  - destination: http://registry:5000/cpa/cpvpa
    match:
      semver: '>= v0.8.4'
    source: registry.k8s.io/cpa/cpvpa
  - destination: http://registry:5000/kube-proxy
    match:
      semver: '>= v1.29.0'
    source: registry.k8s.io/kube-proxy
  - destination: http://registry:5000/metrics-server/metrics-server
    match:
      semver: '>= v0.7.2'
    source: registry.k8s.io/metrics-server/metrics-server
  - destination: http://registry:5000/node-problem-detector/node-problem-detector
    match:
      semver: '>= v0.8.22'
    source: registry.k8s.io/node-problem-detector/node-problem-detector
  - destination: http://registry:5000/sig-storage/csi-attacher
    match:
      semver: '>= v4.4.0'
    source: registry.k8s.io/sig-storage/csi-attacher
  - destination: http://registry:5000/sig-storage/csi-node-driver-registrar
    match:
      semver: '>= v2.9.0'
    source: registry.k8s.io/sig-storage/csi-node-driver-registrar
  - destination: http://registry:5000/sig-storage/csi-provisioner
    match:
      semver: '>= v5.2.0'
    source: registry.k8s.io/sig-storage/csi-provisioner
  - destination: http://registry:5000/sig-storage/csi-resizer
    match:
      semver: '>= v1.13.2'
    source: registry.k8s.io/sig-storage/csi-resizer
  - destination: http://registry:5000/sig-storage/csi-snapshotter
    match:
      semver: '>= v8.2.1'
    source: registry.k8s.io/sig-storage/csi-snapshotter
  - destination: http://registry:5000/sig-storage/snapshot-controller
    match:
      semver: '>= v8.2.1'
    source: registry.k8s.io/sig-storage/snapshot-controller
  - destination: http://registry:5000/sig-storage/livenessprobe
    match:
      semver: '>= v2.12.0'
    source: registry.k8s.io/sig-storage/livenessprobe
  - destination: http://registry:5000/coredns/coredns
    match:
      semver: '>= v1.12.4'
    source: registry.k8s.io/coredns/coredns
  - destination: http://registry:5000/gardener-project/releases/gardener/coredns-config-adapter
    match:
      semver: '>= v0.4.0'
    source: europe-docker.pkg.dev/gardener-project/releases/gardener/coredns-config-adapter
  - destination: http://registry:5000/dns/k8s-dns-node-cache
    match:
      semver: '>= 1.25.0'
    source: registry.k8s.io/dns/k8s-dns-node-cache
  - destination: http://registry:5000/csi-lvm-controller
    match:
      semver: '>= v0.9.0'
    source: r.metal-stack.io/csi-lvm-controller
  - destination: http://registry:5000/csi-lvm-provisioner
    match:
      semver: '>= v0.7.0'
    source: r.metal-stack.io/csi-lvm-provisioner
  - destination: http://registry:5000/droptailer
    match:
      semver: '>= v0.2.19'
    source: r.metal-stack.io/droptailer
  - destination: http://registry:5000/node-init
    match:
      semver: '>= v0.1.8'
    source: r.metal-stack.io/node-init
  - destination: http://registry:5000/netapp/trident
    match:
      semver: '>= 25.06.0'
    source: docker.io/netapp/trident
  - destination: http://registry:5000/netapp/trident-autosupport
    match:
      semver: '>= 25.06.0'
    source: docker.io/netapp/trident-autosupport
  - destination: http://registry:5000/netapp/trident-operator
    match:
      semver: '>= 25.06.0'
    source: docker.io/netapp/trident-operator
  - destination: http://registry:5000/library/busybox
    match:
      semver: '>= 1.36'
    source: docker.io/library/busybox
  - destination: http://registry:5000/cilium/cilium
    match:
      semver: '>= 1.17.12'
    source: quay.io/cilium/cilium
  - destination: http://registry:5000/cilium/operator
    match:
      semver: '>= 1.17.12'
    source: quay.io/cilium/operator
  - destination: http://registry:5000/cilium/cilium-envoy
    match:
      tags:
      - v1.34.12-1765374555-6a93b0bbba8d6dc75b651cbafeedb062b2997716
    source: quay.io/cilium/cilium-envoy
  - destination: http://registry:5000/cilium/hubble-relay
    match:
      semver: '>= 1.17.12'
    source: quay.io/cilium/hubble-relay
  - destination: http://registry:5000/cilium/hubble-ui
    match:
      semver: '>= 0.13.3'
    source: quay.io/cilium/hubble-ui
  - destination: http://registry:5000/cilium/hubble-ui-backend
    match:
      semver: '>= 0.13.3'
    source: quay.io/cilium/hubble-ui-backend
  - destination: http://registry:5000/cilium/certgen
    match:
      semver: '>= 0.3.2'
    source: quay.io/cilium/certgen
# Image name of the oci-mirror. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
isolated_clusters_registry_oci_mirror_image_name: null
# Image tag of the oci-mirror. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
isolated_clusters_registry_oci_mirror_image_tag: null
# Storage class of the registry persistent volume.
isolated_clusters_registry_storage_class_name: null
# Size of the registry persistent volume.
isolated_clusters_registry_storage_size: 100Gi
# Kubeconfig content for accessing the virtual garden. Read from the garden-access secret by default.
isolated_clusters_virtual_garden_kubeconfig: '{{ lookup(''k8s'', api_version=''v1'', kind=''Secret'', namespace=''garden'', resource_name=''garden-kubeconfig-for-admin'').get(''data'', {}).get(''kubeconfig'') | b64decode }}'
```
