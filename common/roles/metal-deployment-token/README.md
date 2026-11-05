# metal-deployment-token

This role can be used to fetch the metal-apiserver admin deployment token intended for deploying infra services. Typically the services to deploy require a dedicated tenant and a specific api token. The token is created by the metal-control-plane helm-chart and stored as a secret in the metal-control-plane namespace where the metal-apiserver is running. So, it is required to have a connection to the Kubernetes cluster where the metal-apiserver is running.

For partition deployments we recommend to just provide a deployment token issued by hand and store this token in the deployment variables.

All tasks for this are run on the deployment machine (`localhost`). The token is then exported with the name `metal_deployment_admin_token` as an Ansible fact for the `localhost`.

Please note that the created token has admin privileges by nature and expires after 8 hours. It should not be stored on a target host.

## Requirements

- The metal-stack V2 API client needs to be installed (see [metal-v2-client role](../metal-v2-client/))

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# The admin token to use for deployment. When unset, it is read from the referenced secret.
metal_deployment_admin_token: null
# Key within the secret data that contains the token.
metal_deployment_token_secret_key: admin_editor_token
# Name of the secret containing the metal-apiserver admin token.
metal_deployment_token_secret_name: metal-apiserver-admin-token
# Namespace of the secret containing the metal-apiserver admin token.
metal_deployment_token_secret_namespace: '{{ metal_control_plane_namespace }}'
```
