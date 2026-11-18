# gardener-extensions

Deploys Gardener operator extension resources into the Gardener runtime cluster.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# Additional CIDRs that are always allowed by the acl extension.
gardener_extension_acl_additional_allowed_cidrs: []
# Whether the acl extension is registered.
gardener_extension_acl_enabled: false
# Tag of the acl extension helm chart.
gardener_extension_acl_helm_chart_tag: '{{ gardener_extension_acl_image_tag }}'
# Tag of the acl admission application helm chart.
gardener_extension_admission_acl_helm_chart_application_tag: '{{ gardener_extension_acl_image_tag }}'
# Tag of the acl admission runtime helm chart.
gardener_extension_admission_acl_helm_chart_runtime_tag: '{{ gardener_extension_acl_image_tag }}'
# Tag of the calico admission application helm chart.
gardener_extension_admission_calico_helm_chart_application_tag: '{{ gardener_extension_networking_calico_image_tag }}'
# Tag of the calico admission runtime helm chart.
gardener_extension_admission_calico_helm_chart_runtime_tag: '{{ gardener_extension_networking_calico_image_tag }}'
# Tag of the cilium admission application helm chart.
gardener_extension_admission_cilium_helm_chart_application_tag: '{{ gardener_extension_networking_cilium_image_tag }}'
# Tag of the cilium admission runtime helm chart.
gardener_extension_admission_cilium_helm_chart_runtime_tag: '{{ gardener_extension_networking_cilium_image_tag }}'
# Tag of the gcp admission application helm chart.
gardener_extension_admission_gcp_helm_chart_application_tag: '{{ gardener_extension_provider_gcp_image_tag }}'
# Tag of the gcp admission runtime helm chart.
gardener_extension_admission_gcp_helm_chart_runtime_tag: '{{ gardener_extension_provider_gcp_image_tag }}'
# Tag of the metal admission application helm chart.
gardener_extension_admission_metal_helm_chart_application_tag: '{{ gardener_extension_provider_metal_image_tag }}'
# Tag of the metal admission runtime helm chart.
gardener_extension_admission_metal_helm_chart_runtime_tag: '{{ gardener_extension_provider_metal_image_tag }}'
# Tag of the shoot-dns-service admission application helm chart.
gardener_extension_admission_shoot_dns_service_helm_chart_application_tag: '{{ gardener_extension_shoot_dns_service_image_tag }}'
# Tag of the shoot-dns-service admission runtime helm chart.
gardener_extension_admission_shoot_dns_service_helm_chart_runtime_tag: '{{ gardener_extension_shoot_dns_service_image_tag }}'
# Default webhook mode of the audit extension.
gardener_extension_audit_default_webhook_mode: null
# Whether the audit extension is registered.
gardener_extension_audit_enabled: false
# Tag of the audit extension helm chart.
gardener_extension_audit_helm_chart_tag: '{{ gardener_extension_audit_image_tag }}'
# Whether the backup-s3 extension is registered.
gardener_extension_backup_s3_enabled: false
# Tag of the backup-s3 extension helm chart.
gardener_extension_backup_s3_helm_chart_tag: '{{ gardener_extension_backup_s3_image_tag }}'
# Whether the csi-driver-lvm extension is registered.
gardener_extension_csi_driver_lvm_enabled: false
# Tag of the csi-driver-lvm extension helm chart.
gardener_extension_csi_driver_lvm_helm_chart_tag: '{{ gardener_extension_csi_driver_lvm_image_tag }}'
# Image vector overwrite for the csi-driver-lvm extension.
gardener_extension_csi_driver_lvm_image_vector_overwrite: []
# URL of an external dns controller registration to include.
gardener_extension_dns_external_controller_registration_url: null
# Whether additional network policies are deployed for the dns-powerdns extension.
gardener_extension_dns_powerdns_additional_network_policies: false
# Whether the dns-powerdns extension is registered.
gardener_extension_dns_powerdns_enabled: false
# Tag of the dns-powerdns extension helm chart.
gardener_extension_dns_powerdns_helm_chart_tag: '{{ gardener_extension_dns_powerdns_image_tag }}'
# Whether the duros extension is registered.
gardener_extension_duros_enabled: false
# OCI reference of the duros extension helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
gardener_extension_duros_helm_chart: ghcr.io/metal-stack/charts/gardener-extension-duros
# Tag of the duros extension helm chart.
gardener_extension_duros_helm_chart_tag: v0.0.0-pull-request.1
# Image name of the duros extension.
gardener_extension_duros_image_name: ghcr.io/metal-stack/gardener-extension-duros
# Image tag of the duros extension.
gardener_extension_duros_image_tag: duros-draft
# Per-region duros storage configuration.
gardener_extension_duros_regions_config: {}
# Whether the networking-calico extension is registered.
gardener_extension_networking_calico_enabled: true
# Tag of the networking-calico extension helm chart.
gardener_extension_networking_calico_helm_chart_tag: '{{ gardener_extension_networking_calico_image_tag }}'
# Image vector overwrite for the networking-calico extension.
gardener_extension_networking_calico_image_vector_overwrite: []
# Whether the networking-cilium extension is registered.
gardener_extension_networking_cilium_enabled: true
# Tag of the networking-cilium extension helm chart.
gardener_extension_networking_cilium_helm_chart_tag: '{{ gardener_extension_networking_cilium_image_tag }}'
# Image vector overwrite for the networking-cilium extension.
gardener_extension_networking_cilium_image_vector_overwrite: []
# The ONTAP clusters configured for the ontap extension.
gardener_extension_ontap_clusters: []
# Whether the ontap extension is registered.
gardener_extension_ontap_enabled: false
# Tag of the ontap extension helm chart.
gardener_extension_ontap_helm_chart_tag: '{{ gardener_extension_ontap_image_tag }}'
# Whether the os-metal extension is registered.
gardener_extension_os_metal_enabled: true
# Tag of the os-metal extension helm chart.
gardener_extension_os_metal_helm_chart_tag: '{{ gardener_os_controller_image_tag }}'
# The operating system types handled by the os-metal extension.
gardener_extension_os_metal_types:
- ubuntu
- debian
- nvidia
# Whether the provider-gcp extension is registered.
gardener_extension_provider_gcp_enabled: true
# Tag of the provider-gcp extension helm chart.
gardener_extension_provider_gcp_helm_chart_tag: '{{ gardener_extension_provider_gcp_image_tag }}'
# Additional network policies deployed by the provider-metal extension.
gardener_extension_provider_metal_additional_network_policies: null
# Default pods CIDR defaulted by the provider-metal admission controller.
gardener_extension_provider_metal_admission_default_pods_cidr: null
# Default services CIDR defaulted by the provider-metal admission controller.
gardener_extension_provider_metal_admission_default_services_cidr: null
# Amount of replicas of the provider-metal admission controller.
gardener_extension_provider_metal_admission_replicas: 1
# Whether a vertical pod autoscaler is enabled for the provider-metal admission controller.
gardener_extension_provider_metal_admission_vpa: true
# Duros storage configuration of the provider-metal extension.
gardener_extension_provider_metal_duros_storage_config: null
# Whether duros storage integration is enabled in the provider-metal extension.
gardener_extension_provider_metal_duros_storage_enabled: false
# Allowed egress destinations for shoot control planes.
gardener_extension_provider_metal_egress_destinations: []
# Whether the provider-metal extension is registered.
gardener_extension_provider_metal_enabled: true
# Backup schedule of the shoot control plane etcd.
gardener_extension_provider_metal_etcd_backup_schedule: 0 */2 * * *
# Delta snapshot period of the shoot control plane etcd.
gardener_extension_provider_metal_etcd_delta_snapshot_period: 5m
# Storage class of the shoot control plane etcd.
gardener_extension_provider_metal_etcd_storage_class_name: null
# Whether etcd pods are evicted on volume issues.
gardener_extension_provider_metal_etcd_volume_eviction: false
# Internal network prefixes for firewall rules of the provider-metal extension.
gardener_extension_provider_metal_firewall_internal_prefixes: []
# Tag of the provider-metal extension helm chart.
gardener_extension_provider_metal_helm_chart_tag: '{{ gardener_extension_provider_metal_image_tag }}'
# Image pull policy for the provider-metal extension containers.
gardener_extension_provider_metal_image_pull_policy: '{{ metal_control_plane_image_pull_policy | default(''IfNotPresent'') }}'
# Image pull secret encoded docker config for the provider-metal extension.
gardener_extension_provider_metal_image_pull_secret: null
# Machine image to firewall image mapping of the provider-metal extension. Defaults to metal_api_images.
gardener_extension_provider_metal_machine_images: '{{ metal_api_images | default([]) }}'
# Whether the shoot-cert-service extension is registered.
gardener_extension_shoot_cert_service_enabled: true
# Tag of the shoot-cert-service extension helm chart.
gardener_extension_shoot_cert_service_helm_chart_tag: '{{ gardener_extension_shoot_cert_service_image_tag }}'
# Email address of the ACME issuer account. Required when the shoot-cert-service extension is enabled.
gardener_extension_shoot_cert_service_issuer_email: null
# Private key of the ACME issuer account.
gardener_extension_shoot_cert_service_issuer_private_key: ''
# ACME server URL of the certificate issuer.
gardener_extension_shoot_cert_service_issuer_server: https://acme-v02.api.letsencrypt.org/directory
# Nameservers used for DNS prechecks of the shoot-cert-service extension.
gardener_extension_shoot_cert_service_precheck_nameservers: []
# Whether custom issuers can be configured in shoots.
gardener_extension_shoot_cert_service_shoot_issuers_enabled: false
# Whether the shoot-dns-service extension is registered.
gardener_extension_shoot_dns_service_enabled: true
# Tag of the shoot-dns-service extension helm chart.
gardener_extension_shoot_dns_service_helm_chart_tag: '{{ gardener_extension_shoot_dns_service_image_tag }}'
# Image name override of the dns-controller-manager.
gardener_shoot_dns_service_dns_controller_manager_image_name: null
# Image tag override of the dns-controller-manager.
gardener_shoot_dns_service_dns_controller_manager_image_tag: null
# Whether DNS provider replication is enabled in the shoot-dns-service extension.
gardener_shoot_dns_service_dns_provider_replication: false
# Image vector overwrite for the shoot-dns-service extension.
gardener_shoot_dns_service_image_vector_overwrite: []
```
