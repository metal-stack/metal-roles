# isolated clusters

Contains roles for deploying addtional services for the isolated cluster feature as described [here](https://docs.metal-stack.io/stable/overview/isolated-kubernetes/).

It contains the services:

- oci-mirror
- Registry
- DNS
- NTP

A cert-manager is expected to be deployed by the user beforehand.

## Variables

The `control-plane-defaults` folder contains defaults that are used by multiple roles in the control-plane directory. You can look up all the default values [here](control-plane-defaults/main.yaml).

| Name                                                             | Mandatory | Description                                                                                      |
| ---------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| isolated_clusters_virtual_garden_kubeconfig                      |           | The kubeconfig to access the virutal garden as a string value.                                              |
| isolated_clusters_ntp_image_name                                 |           | The image name of the ntp service for the partition.                                             |
| isolated_clusters_ntp_image_tag                                  | yes       | The tag or version of the ntp service container image.                                           |
| isolated_clusters_ntp_namespace                                  |           | The namespace to deploy the ntp server to.                                                       |
| isolated_clusters_dns_image_name                                 |           | The image name of the dns service for the partition.                                             |
| isolated_clusters_dns_image_tag                                  | yes       | The tag or version of the dns service container image.                                           |
| isolated_clusters_dns_namespace                                  |           | The namespace to deploy the dns server to.                                                       |
| isolated_clusters_ingress_controller_namespace                   |           | The namespace where the ingress controller should be deployed to.                                |
| isolated_clusters_ingress_controller_chart_version               | yes       | The version of the ingress controller chart.                                                     |
| isolated_clusters_ingress_controller_chroot                      |           | Indicates if the image should have a changed root.                                               |
| isolated_clusters_ingress_controller_load_balancer_ip            | yes       | The load balancer source ip of the ingress controller.                                           |
| isolated_clusters_ingress_controller_load_balancer_source_ranges | yes       | The load balancer source ranges of the ingress controller.                                       |
| isolated_clusters_registry_image_name                            |           | The image name of the registry service for the partition.                                        |
| isolated_clusters_registry_image_tag                             | yes       | The tag or version of the registry service container image.                                      |
| isolated_clusters_registry_namespace                             |           | The namespace for the registry used for isolated clusters.                                       |
| isolated_clusters_registry_oci_mirror_image_name                 |           | The OCI mirror image of the registry used for isolated clusters.                                 |
| isolated_clusters_registry_oci_mirror_image_tag                  | yes       | The OCI mirror version of the registry used for isolated clusters.                               |
| isolated_clusters_registry_oci_mirror_config                     |           | Contains a mapping of source and destination images for specific versions.                       |
| isolated_clusters_registry_storage_size                          |           | The storage size of the registry used for isolated clusters.                                     |
| isolated_clusters_registry_storage_class_name                    |           | The storageClassName of the registry used for isolated clusters.                                 |
| isolated_clusters_registry_ingress_fqdn                          | yes       | The full name of the registry used for isolated clusters.                                        |
| isolated_clusters_registry_ingress_annotations                   |           | Optional ingress annotations for the registry used for isolated clusters.                        |
| isolated_clusters_partition_services_cluster                     |           | The cluster to deploy the services like ntp, dns, ingress, cert manager and the OCI registry to. |
