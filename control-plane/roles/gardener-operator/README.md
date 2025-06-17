# gardener-operator

Deploys the Gardener Operator into the Garden cluster. This role spins up a virtual garden.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Migration Path

If you are still using the `gardener` role for setting up the Gardener, please read the following notes for the migration to the Gardener Operator.

1. Prepare the Gardener Operator setup
  - Ideally, create a dedicated cluster for hosting the Gardener control plane. It is possible to also host the Gardener installation in the same cluster as the metal-stack control plane, but it is not recommended for production scenarios.
  - Prepare the new playbook that uses the roles `gardener-operator`, `gardener-cloud-profile`, `gardener-extensions` and optionally `gardener-gardenlet`. Parametrize these roles properly.
2. Scale down the existing virtual garden and take a last backup of the Garden ETCD
  - `kubectl scale deployment garden-kube-apiserver --replicas 0`
  - `kubectl exec -it <virtual-garden-etcd-sts>-0 -c backup-restore -- curl -k 'http://localhost:8080/snapshot/full?final=true'`
  - `kubectl scale sts <virtual-garden-etcd-sts> --replicas 0`
3. Copy over the ETCD backup to a new folder in the backup infrastructure
  - The object prefix changed from `etcd-<stage>-etcd` to `virtual-garden-etcd-main/etcd-main`
  - In case of using GCP copy over to the new naming scheme recursively: `gsutil cp -r gs://<etcd-backup-folder>/etcd-test-etcd/v2 gs://<etcd-backup-folder>/virtual-garden-etcd-main/etcd-main/v2`

## Variables

| Name                                                          | Mandatory | Description                                                                                                                                                                                  |
| ------------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_operator_image_name                                  |           | The gardener-operator container image name                                                                                                                                                   |
| gardener_operator_image_tag                                   |           | The gardener-operator container image tag                                                                                                                                                    |
| gardener_operator_backup_infrastructure                       |           | The backup infrastructure configuration for the virtual garden                                                                                                                               |
| gardener_operator_backup_infrastructure_secret                |           | The backup infrastructure secret for the virtual garden                                                                                                                                      |
| gardener_operator_dns_providers                               |           | The dns providers that are used when spinning up the virtual garden                                                                                                                          |
| gardener_operator_garden_name                                 |           | The name of the garden resource                                                                                                                                                              |
| gardener_operator_repo_url                                    |           | The repo url of the Gardener project where the operator chart is located                                                                                                                     |
| gardener_operator_repo_ref                                    |           | The repo ref of the Gardener project where the operator chart is located                                                                                                                     |
| gardener_operator_local_tmp_dir                               |           | A local checkout path for the Gardener git repository                                                                                                                                        |
| gardener_operator_high_availability_control_plane             |           | Whether or not to deploy the Gardener control plane in HA configuration                                                                                                                      |
| gardener_operator_ingress_dns_domain                          | true      | The domain on which the ingress-nginx (i.e. monitoring) is exposed                                                                                                                           |
| gardener_operator_virtual_garden_public_dns                   |           | The domain on which the virtual garden istio ingress is exposed                                                                                                                              |
| gardener_operator_virtual_garden_etcd_storage_class           |           | The storage class used by the virtual garden etcd                                                                                                                                            |
| gardener_virtual_garden_api_server_version                    |           | The kubernetes version of the virtual garden                                                                                                                                                 |
| gardener_operator_virtual_garden_oidc_issuer_url              |           | [Corresponds to the `--oidc-issuer-url` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-issuer-url) in the Kubernetes API server configuration.           |
| gardener_operator_virtual_garden_oidc_client_id               |           | [Corresponds to the `--oidc-client-id` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-client-id) in the Kubernetes API server configuration.             |
| gardener_operator_virtual_garden_oidc_username_claim          |           | [Corresponds to the `--oidc-username-claim` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-username-claim) in the Kubernetes API server configuration.   |
| gardener_operator_virtual_garden_oidc_username_prefix         |           | [Corresponds to the `--oidc-username-prefix` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-username-prefix) in the Kubernetes API server configuration. |
| gardener_operator_virtual_garden_oidc_groups_claim            |           | [Corresponds to the `--oidc-groups-claim` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-claim) in the Kubernetes API server configuration.       |
| gardener_operator_virtual_garden_oidc_groups_prefix           |           | [Corresponds to the `--oidc-groups-prefix` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-prefix) in the Kubernetes API server configuration.     |
| gardener_operator_virtual_garden_oidc_ca                      |           | [Corresponds to the `--oidc-ca-file` flag](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#oidc-groups-prefix) in the Kubernetes API server configuration.           |
| gardener_operator_patch_istio_ingress_gateway_service_ip      |           | For local environments: patch the virtual garden ingress ip to continue with the deployment                                                                                                  |
| gardener_operator_expose_virtual_garden_through_ingress_nginx |           | For local environments: expose the virtual garden through nginx-ingress                                                                                                                      |
