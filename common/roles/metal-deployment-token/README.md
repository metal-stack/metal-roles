# metal-deployment-token

This role can be used to create a short-lives admin deployment token intended for deploying infra services. Typically these require a dedicated tenant and a specific api token. The token is created through the metal-apiserver CLI through Kubernetes pod exec. So, it is required to have a connection to the Kubernetes cluster where the metal-apiserver is running.

All tasks for this are run on the deployment machine (`localhost`). The token is then exported with the name `metal_deployment_admin_token` as an Ansible fact for the `localhost`.

If a connection to the control plane Kubernetes cluster is unwanted, another option for the deployment would be to create a long-lived token for the deployment and just set `metal_deployment_admin_token` in `host_vars` for `localhost`. Then this role can be quickly swapped in or out.

Please note that the created token has admin privileges by nature and expires fairly quickly. The created token is only intended to live during a CI deployment. It should not be stored on a target host.

## Requirements

- The metal-stack V2 API client needs to be installed (see [metal-v2-client role](../metal-v2-client/))

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                              | Mandatory | Description                         |
| --------------------------------- | --------- | ----------------------------------- |
| metal_deployment_token_admin_role |           | The admin role to be created        |
| metal_deployment_token_expiration |           | The expiration of the created token |
