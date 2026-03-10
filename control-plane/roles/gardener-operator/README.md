# gardener-operator

Deploys the Gardener Operator into the Garden cluster. This role spins up a virtual garden.

Please refer to the metal-stack gardener integration in our [documentation](https://docs.metal-stack.io/stable/overview/kubernetes/).

Check out the Gardener project for further documentation on [gardener.cloud](https://gardener.cloud/).

## Migration Path

If you are still using the `gardener` role for setting up the Gardener, please read the following notes for the migration to the Gardener Operator.

> [!CAUTION]
> The migration requires a downtime of the Gardener for end-users. The API servers of the end-users are not disrupted.

> [!IMPORTANT]
> For the migration it is required to either wait until Gardener `v1.119` or use a backport feature to `force-redeploy` the existing Gardenlets. If you want to use the backports, please set the following overwrites:
>
> ```yaml
> gardener_apiserver_image_tag: gardenlet-forceful-redeployment
> gardener_apiserver_image_name: r.metal-stack.io/gardener/gardener-apiserver
> gardener_operator_image_tag: gardenlet-forceful-redeployment
> gardener_operator_image_name: r.metal-stack.io/gardener/operator
> ```

Here are the steps for the migration:

1. Prepare the Gardener Operator setup
    - Ideally, create a dedicated cluster for hosting the Gardener control plane. It is possible to also host the Gardener installation in the same cluster as the metal-stack control plane, but it is not recommended for production scenarios.
    - Prepare the new playbook that uses the roles `gardener-operator`, `gardener-cloud-profile`, `gardener-extensions`, `gardener-virtual-garden-access`, `gardener-projects`, `gardener-gardenlet`, `gardener-shoots` and `gardener-managed-seeds`. Parametrize them properly. Many parameters are equivalent as they were before, but the new roles require new ones. Check them all.
1. Scale down the existing virtual garden and take a last backup of the Garden ETCD
    - `kubectl scale deployment garden-kube-apiserver --replicas 0`
    - `kubectl exec -it <virtual-garden-etcd-sts>-0 -c backup-restore -- curl -k 'http://localhost:8080/snapshot/full?final=true'`
    - `kubectl scale sts <virtual-garden-etcd-sts> --replicas 0`
1. Copy over the ETCD backup to a new folder in the backup infrastructure
    - The object prefix changed from `etcd-<stage>-etcd` to `virtual-garden-etcd-main/etcd-main`
    - In case of using GCP copy over to the new naming scheme recursively: `gcloud storage cp -r gs://<etcd-backup-folder>/<virtual-garden-etcd-sts>/v2 gs://<etcd-backup-folder>/virtual-garden-etcd-main/etcd-main/v2`
1. ️⚠️ If you migrate from a standalone ETCD it is necessary to explicitly set `gardener_operator_high_availability_control_plane` to `false`. After the initial deployment of the virtual garden was successful, you can toggle this field to `true` in order to migrate to HA control plane. In case you deployed this without following this instruction, please repair your ETCD as described in [Recovering Etcd Clusters](https://gardener.cloud/docs/other-components/etcd-druid/recovering-etcd-clusters/).
1. Deploy the roles `gardener-operator`, `gardener-extensions`, `gardener-virtual-garden-access` and `gardener-cloud-profile` (order matters).
    - In case the `etcd-druid` does not start reconciling the `ETCD` resource for the virtual garden, you might have to manually add the finalizer `druid.gardener.cloud/etcd-druid` on the `ETCD` resource.
1. Manually deploy a kubeconfig secret for remote Gardenlet deployment through the Gardener Operator into the Virtual Garden as described [here](https://gardener.cloud/docs/gardener/deployment/deploy_gardenlet_via_operator/#remote-clusters). Delete the old Gardenlet helm chart from the original Gardener cluster and deploy the Gardenlet through the `gardener-gardenlet` role. Don't forget to specify the `gardenClientConnection.gardenClusterAddress` (see https://github.com/gardener/gardener/pull/11996)
    - The gardenlet name needs to be identical with the old name of the initial seed in order to take over the existing resources. Usually, we used the name of the stage for this seed.
1. If you did not take over the existing certificates from the previous Virtual Garden, it might be necessary to run `kubectl --context garden annotate managedseeds -n garden <managed-seed-resource> gardener.cloud/operation=renew-kubeconfig` in order to fix the Gardenlet deployments.
1. Reconcile your shoots, this should end up in a stable setup.
1. Deploy the `gardener-projects`, `gardener-shoots` and `gardener-managed-seeds` roles for deploying your shooted seeds.
1. To complete the migration, deploy a new Gardenlet either in a dedicated cluster or again in the Gardener cluster and execute a shoot migration of the shooted seeds to the new cluster. Follow [this document](https://github.com/gardener/gardener/blob/master/docs/operations/control_plane_migration.md#triggering-the-migration). For us, it was also necessary to edit the status of the shoot and add the missing `pods` and `services` CIDR as otherwise the proposed command from the Gardener documentation fails.
1. As the shoot migration for metal-stack is not fully working, you need to roll the firewalls of the seeds. Pay attention that the userdata of the firewall gets newly generated by the firewall-controller-manager such that it contains the new kubeconfig to contact the seed api-server.
    - In case the `keep-worker` annotation was used on a shooted seed and you want to prevent the seed worker nodes to roll, you need to set the annotation `cluster.metal-stack.io/use-worker-hash-<group-name>: <group-hash>`.

![Migration Path](./migration.drawio.svg)

## Variables

| Name                                                          | Mandatory | Description                                                                                                                                                                                  |
| ------------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gardener_operator_image_name                                  |           | The gardener-operator container image name                                                                                                                                                   |
| gardener_operator_image_tag                                   |           | The gardener-operator container image tag                                                                                                                                                    |
| gardener_operator_helm_chart_tag                              |           | The gardener-operator helm chart image tag                                                                                                                                                   |
| gardener_operator_backup_infrastructure                       |           | The backup infrastructure configuration for the virtual garden                                                                                                                               |
| gardener_operator_backup_infrastructure_secret                |           | The backup infrastructure secret for the virtual garden                                                                                                                                      |
| gardener_operator_runtime_cluster_provider                    |           | The provider of the runtime cluster in the garden resource                                                                                                                                   |
| gardener_operator_dns_providers                               |           | The dns providers that are used when spinning up the virtual garden                                                                                                                          |
| gardener_operator_garden_name                                 |           | The name of the garden resource                                                                                                                                                              |
| gardener_operator_repo_url                                    |           | The repo url of the Gardener project where the operator chart is located                                                                                                                     |
| gardener_operator_repo_ref                                    |           | The repo ref of the Gardener project where the operator chart is located                                                                                                                     |
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
| gardener_operator_expose_virtual_garden_through_ingress_nginx |           | For local environments: expose the virtual garden through nginx-ingress                                                                                                                      |
