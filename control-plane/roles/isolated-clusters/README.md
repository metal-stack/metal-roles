# partition services

Contains roles for deploying addtional services for the partition.

## Variables

The `control-plane-defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all the default values [here](control-plane-defaults/main.yaml).

| Name                                                                     | Mandatory | Description                                                                                      |
| ------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------ |
| isolated_clusters_ntp_image_name                                         |           | The image name of the ntp service for the partition.                                             |
| isolated_clusters_ntp_image_tag                                          | yes       | The tag or version of the ntp service container image.                                           |
| isolated_clusters_ntp_namespace                                          |           | The namespace to deploy the ntp server to.                                                       |
| isolated_clusters_dns_image_name                                         |           | The image name of the dns service for the partition.                                             |
| isolated_clusters_dns_image_tag                                          | yes       | The tag or version of the dns service container image.                                           |
| isolated_clusters_dns_namespace                                          |           | The namespace to deploy the dns server to.                                                       |
| isolated_clusters_ingress_ingress_controller_namespace                   |           | The namespace where the ingress controller should be deployed to.                                |
| isolated_clusters_ingress_ingress_controller_chart_version               | yes       | The version of the ingress controller chart.                                                     |
| isolated_clusters_ingress_ingress_controller_chroot                      |           | Indicates if the image should have a changed root.                                               |
| isolated_clusters_ingress_ingress_controller_load_balancer_source_ranges | yes       | The load balancer source ranges of the ingress controller.                                       |
| isolated_clusters_ingress_cert_manager_version                           | yes       | The cert manager version used to generate certificates.                                          |
| isolated_clusters_ingress_cert_manager_cluster_issuer                    |           | The cluster issuer for the cert manager.                                                         |
| isolated_clusters_ingress_cert_manager_lets_encrypt_expiry_mail_address  | yes       | The email that should receive certificate expiry warnings.                                       |
| isolated_clusters_registry_namespace                                     |           | The namespace for the registry used for isolated clusters.                                       |
| isolated_clusters_registry_version                                       | yes       | The version of the registry used for isolated clusters.                                          |
| isolated_clusters_registry_oci_mirror_version                            | yes       | The OCI mirror version of the registry used for isolated clusters.                               |
| isolated_clusters_registry_storage_size                                  |           | The storage size of the registry used for isolated clusters.                                     |
| isolated_clusters_registry_ingress_fqdn                                  | yes       | The full name of the registry used for isolated clusters.                                        |
| isolated_clusters_partition_services_cluster                             |           | The cluster to deploy the services like ntp, dns, ingress, cert manager and the OCI registry to. |
