# gardener-extensions

Deploys Gardener operator extension resources into the Gardener runtime cluster.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

### gardener-extension-acl

| Name                                                        | Mandatory | Description                                                                                             |
| ----------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_acl_enabled                              |           | If enabled, deploys the extension                                                                       |
| gardener_extension_acl_helm_chart                           |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_acl_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_acl_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_acl_helm_chart_tag                       |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_acl_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_acl_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_acl_image_name                           |           | Setting an explicit image name for the gardener-extension-acl                                           |
| gardener_extension_acl_image_tag                            |           | Setting an explicit image tag for the gardener-extensionacl                                             |
| gardener_extension_acl_additional_allowed_cidrs             |           | Additional allowed CIDRs to add when the extension gets enabled on a kube-apiserver                     |

### gardener-extension-audit

| Name                                    | Mandatory | Description                                                     |
| --------------------------------------- | --------- | --------------------------------------------------------------- |
| gardener_extension_audit_enabled        |           | If enabled, deploys the extension                               |
| gardener_extension_audit_helm_chart     |           | The ref to the helm oci artifact to deploy this extension       |
| gardener_extension_audit_helm_chart_tag |           | The tag of the helm oci artifact to deploy this extension       |
| gardener_extension_audit_image_name     |           | Setting an explicit image name for the gardener-extension-audit |
| gardener_extension_audit_image_tag      |           | Setting an explicit image tag for the gardener-extension-audit  |

### gardener-extension-backup-s3

| Name                                        | Mandatory | Description                                                         |
| ------------------------------------------- | --------- | ------------------------------------------------------------------- |
| gardener_extension_backup_s3_enabled        |           | If enabled, deploys the extension                                   |
| gardener_extension_backup_s3_helm_chart     |           | The ref to the helm oci artifact to deploy this extension           |
| gardener_extension_backup_s3_helm_chart_tag |           | The tag of the helm oci artifact to deploy this extension           |
| gardener_extension_backup_s3_image_name     |           | Setting an explicit image name for the gardener-extension-backup-s3 |
| gardener_extension_backup_s3_image_tag      |           | Setting an explicit image tag for the gardener-extension-backup-s3  |

### gardener-extension-csi-driver-lvm

| Name                                             | Mandatory | Description                                                              |
| ------------------------------------------------ | --------- | ------------------------------------------------------------------------ |
| gardener_extension_csi_driver_lvm_enabled        |           | If enabled, deploys the extension                                        |
| gardener_extension_csi_driver_lvm_helm_chart     |           | The ref to the helm oci artifact to deploy this extension                |
| gardener_extension_csi_driver_lvm_helm_chart_tag |           | The tag of the helm oci artifact to deploy this extension                |
| gardener_extension_csi_driver_lvm_image_name     |           | Setting an explicit image name for the gardener-extension-csi-driver-lvm |
| gardener_extension_csi_driver_lvm_image_tag      |           | Setting an explicit image tag for the  gardener-extension-csi-driver-lvm |

### gardener-extension-dns-powerdns

| Name                                                        | Mandatory | Description                                                                                                   |
| ----------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| gardener_extension_dns_powerdns_enabled                     |           | If enabled, deploys the extension                                                                             |
| gardener_extension_dns_powerdns_helm_chart                  |           | The ref to the helm oci artifact to deploy this extension                                                     |
| gardener_extension_dns_powerdns_helm_chart_tag              |           | The tag of the helm oci artifact to deploy this extension                                                     |
| gardener_extension_dns_powerdns_additional_network_policies |           | Deploys additional network policies required if powerdns runs in the same cluster as the extension controller |
| gardener_extension_dns_powerdns_image_name                  |           | Setting an explicit image name for the gardener-extension-dns-powerdns                                        |
| gardener_extension_dns_powerdns_image_tag                   |           | Setting an explicit image tag for the  gardener-extension-dns-powerdns                                        |

### gardener-extension-networking-calico

| Name                                                           | Mandatory | Description                                                                                             |
| -------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_networking_calico_enabled                   |           | If enabled, deploys the extension                                                                       |
| gardener_extension_networking_calico_helm_chart                |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_calico_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_calico_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_networking_calico_helm_chart_tag            |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_calico_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_calico_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |

### gardener-extension-networking-cilium

| Name                                                           | Mandatory | Description                                                                                             |
| -------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_networking_cilium_enabled                   |           | If enabled, deploys the extension                                                                       |
| gardener_extension_networking_cilium_helm_chart                |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_cilium_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_cilium_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_networking_cilium_helm_chart_tag            |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_cilium_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_cilium_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_networking_cilium_image_vector_overwrite    |           | Allows overriding the image vector for the networking cilium extension                                  |

### os-metal-extension

| Name                                       | Mandatory | Description                                               |
| ------------------------------------------ | --------- | --------------------------------------------------------- |
| gardener_extension_os_metal_enabled        |           | If enabled, deploys the extension                         |
| gardener_extension_os_metal_helm_chart     |           | The ref to the helm oci artifact to deploy this extension |
| gardener_extension_os_metal_helm_chart_tag |           | The tag of the helm oci artifact to deploy this extension |

### gardener-extension-provider-gcp

| Name                                                        | Mandatory | Description                                                                                             |
| ----------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_provider_gcp_enabled                     |           | If enabled, deploys the extension                                                                       |
| gardener_extension_provider_gcp_helm_chart                  |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_gcp_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_gcp_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_provider_gcp_helm_chart_tag              |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_gcp_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_gcp_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |

### gardener-extension-provider-metal

| Name                                                          | Mandatory | Description                                                                                             |
| ------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_provider_metal_enabled                     |           | If enabled, deploys the extension                                                                       |
| gardener_extension_provider_metal_helm_chart                  |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_metal_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_metal_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_provider_metal_helm_chart_tag              |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_metal_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_metal_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_provider_metal_etcd_storage_class_name     |           | The storage class used for metal-stack shoot ETCDs                                                      |
| gardener_extension_provider_metal_etcd_backup_schedule        |           | The backup schedule for metal-stack shoot ETCDs                                                         |
| gardener_extension_provider_metal_etcd_delta_snapshot_period  |           | The delta snapshot period for metal-stack shoot ETCDs                                                   |
| gardener_extension_provider_metal_egress_destinations         |           | Sets allowed egress destinations for the `RestrictEgress` control plane feature gate of the GEPM        |
| gardener_extension_provider_metal_machine_images              |           | Specifies the machine images that are usually the same as in the cloud profile                          |
| gardener_extension_provider_metal_duros_storage_enabled       |           | Enables the duros storage integration feature gate of the GEPM (Lightbits storage)                      |
| gardener_extension_provider_metal_duros_storage_config        |           | Configuration for the duros storage integration                                                         |
| gardener_extension_provider_metal_image_pull_policy           |           | Sets the image pull policy for components deployed through this extension controller.                   |
| gardener_extension_provider_metal_image_pull_secret           |           | Provide image pull secrets for deployed containers                                                      |
| gardener_extension_provider_metal_admission_replicas          |           | Specifies the amount of metal-admission webhook replicas                                                |
| gardener_extension_provider_metal_admission_vpa               |           | Enables the VPA for the metal-admission webhook                                                         |

### shoot-cert-service

| Name                                                        | Mandatory | Description                                                                                                 |
| ----------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| gardener_extension_shoot_cert_service_enabled               |           | If enabled, deploys the extension                                                                           |
| gardener_extension_shoot_cert_service_helm_chart            |           | The ref to the helm oci artifact to deploy this extension                                                   |
| gardener_extension_shoot_cert_service_helm_chart_tag        |           | The tag of the helm oci artifact to deploy this extension                                                   |
| gardener_extension_shoot_cert_service_issuer_private_key    |           | The Let's Encrypt private key used by the cert-management extension controller to setup signed certificates |
| gardener_extension_shoot_cert_service_issuer_email          |           | The issuer email used by the cert-management extension                                                      |
| gardener_extension_shoot_cert_service_issuer_server         |           | The issuer server used by the cert-management extension                                                     |
| gardener_extension_shoot_cert_service_precheck_nameservers  |           | To provide special set of nameservers to be used for prechecking DNSChallenges for an issuer                |
| gardener_extension_shoot_cert_service_shoot_issuers_enabled |           | If enabled, allows to specify issuers in the shoot clusters                                                 |
| gardener_extension_shoot_cert_service_image_name            |           | Setting an explicit image name                                                                              |
| gardener_extension_shoot_cert_service_image_tag             |           | Setting an explicit image tag                                                                               |

### shoot-dns-service

| Name                                                                      | Mandatory | Description                                                                                             |
| ------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------- |
| gardener_extension_shoot_dns_service_enabled                              |           | If enabled, deploys the extension                                                                       |
| gardener_extension_shoot_dns_service_helm_chart                           |           | The ref to the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_shoot_dns_service_helm_chart_runtime         |           | The ref to the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_shoot_dns_service_helm_chart_application     |           | The ref to the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_shoot_dns_service_helm_chart_tag                       |           | The tag of the helm oci artifact to deploy this extension                                               |
| gardener_extension_admission_shoot_dns_service_helm_chart_runtime_tag     |           | The tag of the helm oci artifact to deploy this extension's admission controller in the runtime cluster |
| gardener_extension_admission_shoot_dns_service_helm_chart_application_tag |           | The tag of the helm oci artifact to deploy this extension's admission controller in the virtual garden  |
| gardener_extension_shoot_dns_service_image_vector_overwrite               |           | Allows overriding the image vector for the shoot-dns-service extension                                  |
| gardener_extension_shoot_dns_service_dns_controller_manager_image_name    |           | Setting an explicit image name for the dns-controller-manager                                           |
| gardener_extension_shoot_dns_service_dns_controller_manager_image_tag     |           | Setting an explicit image tag for the dns-controller-manager                                            |
| gardener_extension_shoot_dns_service_dns_provider_replication             |           | Enable provider replication feature for the shoot-service-dns extension                                 |
