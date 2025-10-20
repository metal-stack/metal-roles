# metal-deployment-token

This role can be used to create a deployment token intended for deploying infra services. Typically these require a dedicated tenant and a specific api token. The token is created through the metal-apiserver CLI through Kubernetes pod exec. So, it is required to have a connection to the Kubernetes cluster where the metal-apiserver is running.

The token is then exported with the name `metal_deployment_admin_token`.

Please note that the created token has admin privileges by nature and expires fairly quickly. The created token is only intended to live during a CI deployment.

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                              | Mandatory | Description                         |
| --------------------------------- | --------- | ----------------------------------- |
| metal_deployment_token_admin_role |           | The admin role to be created        |
| metal_deployment_token_expiration |           | The expiration of the created token |
