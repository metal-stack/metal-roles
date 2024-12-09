# gardener

Deploys Gardener into a virtual garden along with a dedicated ETCD and a set of extension controllers.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Variables

| Name                                                   | Mandatory | Description                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------ | --------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gardener_image_vector_overwrite                        |           | Allows overriding the image vector to set custom image versions for gardener                                                                                                                                                                                                  |
| gardener_component_image_vector_overwrite              |           | Allows overriding the image vector to set custom image versions for gardenlet components                                                                                                                                                                                      |
| gardener_apiserver_replicas                            |           | Specifies the amount of gardener-apiserver replicas                                                                                                                                                                                                                           |
| gardener_apiserver_vpa                                 |           | Enables the VPA for the gardener-apiserver                                                                                                                                                                                                                                    |
| gardener_apiserver_resources                           |           | Set custom resource definitions for the gardener-apiserver                                                                                                                                                                                                                    |
| gardener_apiserver_feature_gates                       |           | Sets features gates for the gardener-apiserver                                                                                                                                                                                                                                |
| gardener_apiserver_shoot_kubeconfig_max_expiration     |           | Max shoot kubeconfig expiration for the gardener-apiserver                                                                                                                                                                                                                    |
| gardener_controller_manager_resources                  |           | Set custom resource definitions for the gardener-controller-manager                                                                                                                                                                                                           |
| gardener_scheduler_resources                           |           | Set custom resource definitions for the gardener-scheduler                                                                                                                                                                                                                    |
| gardener_dns_domain                                    |           | Specifies the DNS domain on which the Gardener will manage DNS entries                                                                                                                                                                                                        |
| gardener_dns_provider                                  | yes       | Specifies the DNS provider                                                                                                                                                                                                                                                    |
| gardener_backup_infrastructure                         |           | Specifies the Gardener backup infrastructure, required when `gardener_backup_infrastructure_secret` is set                                                                                                                                                                    |
| gardener_backup_infrastructure_secret                  |           | Specifies the secret for the backup infrastructure                                                                                                                                                                                                                            |
| gardener_soil_name                                     |           | The name of the initial `Seed` (used for spinning up shooted seeds)                                                                                                                                                                                                           |
| gardener_soil_kubeconfig_file_path                     |           | The kubeconfig path to the initial seed cluster                                                                                                                                                                                                                               |
| gardener_soil_vertical_pod_autoscaler_enabled          |           | Enables the VPA for the initial seed cluster                                                                                                                                                                                                                                  |
| gardener_soil_project_owner_name                       |           | Specifies the owner name for the project that the initial seed uses to set up shooted seeds                                                                                                                                                                                   |
| gardener_soil_project_members                          |           | Specifies the members of the soil project. Each member requires a `name` and a `role`. Optionally, an array of `roles` and a `kind` field can be specified. The `kind` defaults to `User`. Example: `{"name": "admin", "kind": "Group", "role": "admin", "roles": ["owner"]}` |
| gardener_gardenlet_shoot_concurrent_syncs              |           | Specifies the amount of concurrent shoot syncs for the Gardenlet                                                                                                                                                                                                              |
| gardener_gardenlet_shoot_reconcile_in_maintenance_only |           | Specifies whether to reconcile shoots only in their maintenance time windows for the Gardenlet                                                                                                                                                                                |
| gardener_gardenlet_shoot_respect_sync_period_overwrite |           | Specifies whether to allow sync period overwrites for shoot resources                                                                                                                                                                                                         |
| gardener_shooted_seeds                                 |           | A list of definitions for shooted seeds reconcile by the initial seed cluster, will be turned into `ManagedSeeds`                                                                                                                                                             |
| gardener_shooted_seed_max_pods                         |           | The max pods amount for the shooted seeds                                                                                                                                                                                                                                     |
| gardener_shooted_seed_node_cidr_mask_size              |           | The node CIDR mask size used for the kubelets of the shooted seeds                                                                                                                                                                                                            |
| gardener_shooted_seed_rollout_delay_minutes            |           | An optional delay between shooted seed rollouts (can be used to calm down bigger environments during an update)                                                                                                                                                               |
| gardener_kube_api_server_kubeconfig                    |           | The kubeconfig for the Gardener Kubernetes API (virtual garden apiserver)                                                                                                                                                                                                     |
| gardener_kube_apiserver_kubeconfig_path                |           | The acts on multiple Kubernetes APIs, this is where it puts the kubeconfig of the Gardener Kubernetes API                                                                                                                                                                     |
| gardener_local_tmp_dir                                 |           | The acts on multiple Kubernetes APIs, this is a local folder in the deployment container to store the kubeconfigs (ephemeral)                                                                                                                                                 |
| gardener_logging_enabled                               |           | Specifies whether the logging Gardener logging stack should be activated in the Gardenlet                                                                                                                                                                                     |

### Virtual Garden

These variables are related to spinning up the virtual garden, a dedicated kube-apiserver, kube-controller-manager and ETCD to host all Gardener resources. This one will have no worker nodes and cannot schedule pods.

The deployment chart is taken from [garden-setup](https://github.com/gardener/garden-setup) and follows the same deployment approach.

| Name                                                 | Mandatory | Description                                                                                                                                                                                  |
| ---------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_virtual_api_server_svc_cluster_ip_add       |           | An integer to "guess" a free IP for the service that allows the soil to internally communicate with the virtual garden                                                                       |
| gardener_virtual_api_server_public_dns               |           | The DNS domain to reach the virtual garden API server on                                                                                                                                     |
| gardener_virtual_api_server_healthcheck_static_token | yes       | A static token for healthchecking the virtual garden API server                                                                                                                              |
| gardener_etcd_backup_schedule                        |           | The backup schedule for the virtual garden ETCD                                                                                                                                              |
| gardener_etcd_snapshot_period                        |           | The snapshot period for the virtual garden ETCD                                                                                                                                              |
| gardener_etcd_garbage_collection_period              |           | The priod for garbage collection for the virtual garden ETCD                                                                                                                                 |
| gardener_etcd_resources                              |           | Set custom resource definitions for the virtual garden ETCD                                                                                                                                  |
| gardener_virtual_api_oidc_issuer_url                 |           | [Corresponds to the `--oidc-issuer-url` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-issuer-url) in the Kubernetes API server configuration.           |
| gardener_virtual_api_oidc_client_id                  |           | [Corresponds to the `--oidc-client-id` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-client-id) in the Kubernetes API server configuration.             |
| gardener_virtual_api_oidc_username_claim             |           | [Corresponds to the `--oidc-username-claim` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-username-claim) in the Kubernetes API server configuration.   |
| gardener_virtual_api_oidc_username_prefix            |           | [Corresponds to the `--oidc-username-prefix` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-username-prefix) in the Kubernetes API server configuration. |
| gardener_virtual_api_oidc_groups_claim               |           | [Corresponds to the `--oidc-groups-claim` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-claim) in the Kubernetes API server configuration.       |
| gardener_virtual_api_oidc_groups_prefix              |           | [Corresponds to the `--oidc-groups-prefix` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-prefix) in the Kubernetes API server configuration.     |
| gardener_virtual_api_oidc_ca                         |           | [Corresponds to the `--oidc-ca-file` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-prefix) in the Kubernetes API server configuration.           |

### Cloud Profile

Variables for the metal-stack cloud profile.

| Name                                                       | Mandatory | Description                                                                         |
| ---------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------- |
| gardener_cloud_profile_stage_name                          |           | The name of the metal-stack environment in the cloud profile                        |
| gardener_cloud_profile_metal_api_url                       |           | The URL used by the Gardener to communicate with the metal-api                      |
| gardener_cloud_profile_metal_api_hmac                      | yes       | The admin HMAC used by the Gardener to communicate with the metal-api               |
| gardener_cloud_profile_machine_images                      |           | The machine images available for shoots in the metal-api                            |
| gardener_cloud_profile_firewall_images                     |           | The firewall images available for shoots in the metal-api                           |
| gardener_cloud_profile_firewall_images_from_machine_images |           | If set to true, uses the passed machine images and adds those with firewall feature |
| gardener_cloud_profile_firewall_controller_versions        |           | The available firewall controller versions for metal-stack shoots                   |
| gardener_cloud_profile_kubernetes                          |           | The available Kubernetes versions for metal-stack shoots                            |
| gardener_cloud_profile_machine_types                       |           | The machine types available for shoots in the metal-api                             |
| gardener_cloud_profile_regions                             |           | The regions available for shoots                                                    |
| gardener_cloud_profile_partitions                          |           | The partitions available for shoots                                                 |
| gardener_os_cri_mapping                                    |           | A mapping to add available CRIs to the machine images                               |

### Extensions

These variable parametrize the Gardener extension controllers.

This includes the metal-stack extension provider called [gardener-extension-provider-metal](https://github.com/metal-stack/gardener-extension-provider-metal) (GEPM).

| Name                                                         | Mandatory | Description                                                                                                                                 |
| ------------------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_extension_provider_gcp_enabled                      |           | If enabled, deploys the gardener-extension-provider-metal                                                                                   |
| gardener_extension_os_metal_enabled                          |           | If enabled, deploys the os-metal-extension                                                                                                  |
| gardener_extension_networking_calico_enabled                 |           | If enabled, deploys the gardener-networking-extension-calico                                                                                |
| gardener_extension_networking_cilium_enabled                 |           | If enabled, deploys the gardener-networking-extension-cilium                                                                                |
| gardener_extension_shoot_cert_service_enabled                |           | If enabled, deploys the gardener-extension-shoot-cert-service                                                                               |
| gardener_extension_shoot_dns_service_enabled                 |           | If enabled, deploys the gardener-extension-shoot-dns-service                                                                                |
| gardener_extension_backup_s3_enabled                         |           | If enabled, deploys the gardener-extension-backup-s3                                                                                        |
| gardener_extension_dns_powerdns_enabled                      |           | If enabled, deploys the gardener-extension-dns-powerdns                                                                                     |
| gardener_os_controller_repo_ref                              |           | A repo reference for deploying the [os-metal-extension](https://github.com/metal-stack/os-metal-extension/)                                 |
| gardener_networking_cilium_repo_ref                          |           | A repo reference for deploying the [gardener-extension-networking-cilium](https://github.com/gardener/gardener-extension-networking-cilium) |
| gardener_extension_provider_metal_repo_ref                   |           | A repo reference for deploying the [gardener-extension-provider-metal](https://github.com/metal-stack/gardener-extension-provider-metal)    |
| gardener_shoot_dns_service_repo_ref                          |           | A repo reference for deploying the [gardener-extension-shoot-dns-service](https://github.com/gardener/gardener-extension-shoot-dns-service) |
| gardener_extension_backup_s3_repo_ref                        |           | A repo reference for deploying the [gardener-extension-backup-s3](https://github.com/metal-stack/gardener-extension-backup-s3)              |
| gardener_extension_dns_powerdns_repo_ref                     |           | A repo reference for deploying the [gardener-extension-dns-powerdns](https://github.com/metal-stack/gardener-extension-dns-powerdns)        |
| gardener_metal_admission_replicas                            |           | Specifies the amount of metal-admission webhook replicas                                                                                    |
| gardener_metal_admission_vpa                                 |           | Enables the VPA for the metal-admission webhook                                                                                             |
| gardener_extension_provider_metal_cluster_audit_enabled      |           | Enables the audit functionality of the GEPM                                                                                                 |
| gardener_extension_provider_metal_audit_to_splunk_enabled    |           | Enables the audit to splunk feature gate of the GEPM                                                                                        |
| gardener_extension_provider_metal_audit_to_splunk            |           | Configuration for the audit to splunk feature gate of the GEPM                                                                              |
| gardener_extension_provider_metal_etcd_storage_class_name    |           | The storage class used for metal-stack shoot ETCDs                                                                                          |
| gardener_extension_provider_metal_etcd_backup_schedule       |           | The backup schedule for metal-stack shoot ETCDs                                                                                             |
| gardener_extension_provider_metal_etcd_delta_snapshot_period |           | The delta snapshot period for metal-stack shoot ETCDs                                                                                       |
| gardener_extension_provider_metal_egress_destinations        |           | Sets allowed egress destinations for the `RestrictEgress` control plane feature gate of the GEPM                                            |
| gardener_extension_provider_metal_duros_storage_enabled      |           | Enables the duros storage integration feature gate of the GEPM (Lightbits storage)                                                          |
| gardener_extension_provider_metal_duros_storage_config       |           | Configuration for the duros storage integration                                                                                             |
| gardener_extension_provider_metal_image_pull_policy          |           | Sets the image pull policy for components deployed through this extension controller.                                                       |
| gardener_extension_provider_metal_image_pull_secret          |           | Provide image pull secrets for deployed containers                                                                                          |
| gardener_cert_management_issuer_private_key                  |           | The Let's Encrypt private key used by the cert-management extension controller to setup signed certificates                                 |
| gardener_extension_networking_cilium_image_vector_overwrite  |           | Allows overriding the image vector for the networking cilium extension                                                                      |
| gardener_cert_management_issuer_email                        |           | The issuer email used by the cert-management extension                                                                                      |
| gardener_cert_management_issuer_server                       |           | The issuer server used by the cert-management extension                                                                                     |
| gardener_cert_management_precheck_nameservers                |           | To provide special set of nameservers to be used for prechecking DNSChallenges for an issuer                                                |
| gardener_cert_management_shoot_issuers_enabled               |           | If enabled, allows to specify issuers in the shoot clusters                                                                                 |
| gardener_shoot_dns_service_image_vector_overwrite            |           | Allows overriding the image vector for the shoot-dns-service extension                                                                      |
| gardener_shoot_dns_service_dns_controller_manager_image_name |           | Setting an explicit image name for the dns-controller-manager                                                                               |
| gardener_shoot_dns_service_dns_controller_manager_image_tag  |           | Setting an explicit image tag for the dns-controller-manager                                                                                |
| gardener_shoot_dns_service_dns_provider_replication          |           | Enable provider replication feature for the shoot-service-dns extension                                                                     |
| gardener_extension_backup_s3_image_name                      |           | Setting an explicit image name for the gardener-extension-backup-s3                                                                         |
| gardener_extension_backup_s3_image_tag                       |           | Setting an explicit image tag for the gardener-extension-backup-s3                                                                          |
| gardener_extension_dns_powerdns_image_name                   |           | Setting an explicit image name for the gardener-extension-dns-powerdns                                                                      |
| gardener_extension_dns_powerdns_image_tag                    |           | Setting an explicit image tag for the  gardener-extension-dns-powerdns                                                                      |

### Certificates

Gardener requires quite a lot of certificates, which should be self-signed and have to be generated before the deployment.

We use a small shell script as in the [mini-lab](https://github.com/metal-stack/mini-lab/blob/master/files/certs/roll_certs.sh) to generate the certificates.

| Name                                         | Mandatory | Description |
| -------------------------------------------- | --------- | ----------- |
| gardener_kube_api_server_ca                  | yes       | -           |
| gardener_kube_api_server_ca_key              | yes       | -           |
| gardener_kube_api_server_cert                | yes       | -           |
| gardener_kube_api_server_key                 | yes       | -           |
| gardener_kube_api_server_client_cert         | yes       | -           |
| gardener_kube_api_server_client_key          | yes       | -           |
| gardener_kube_aggregator_client_cert         | yes       | -           |
| gardener_kube_aggregator_client_key          | yes       | -           |
| gardener_kube_controller_manager_client_cert | yes       | -           |
| gardener_kube_controller_manager_client_key  | yes       | -           |
| gardener_admin_client_cert                   | yes       | -           |
| gardener_admin_client_key                    | yes       | -           |
| gardener_service_account_client_key          | yes       | -           |
| gardener_api_server_ca                       | yes       | -           |
| gardener_api_server_cert                     | yes       | -           |
| gardener_api_server_key                      | yes       | -           |
| gardener_admission_controller_ca             | yes       | -           |
| gardener_admission_controller_cert           | yes       | -           |
| gardener_admission_controller_key            | yes       | -           |
| gardener_controller_manager_ca               | yes       | -           |
| gardener_controller_manager_cert             | yes       | -           |
| gardener_controller_manager_key              | yes       | -           |
| gardener_etcd_ca_cert                        | yes       | -           |
| gardener_etcd_cert                           | yes       | -           |
| gardener_etcd_cert_key                       | yes       | -           |
| gardener_etcd_client_cert                    | yes       | -           |
| gardener_etcd_client_key                     | yes       | -           |
