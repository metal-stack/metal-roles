# metal-deployment-token

This role can be used to fetch the metal-apiserver admin deployment token intended for deploying infra services. Typically the services to deploy require a dedicated tenant and a specific api token. The token is created by the metal-control-plane helm-chart and stored as a secret in the metal-control-plane namespace where the metal-apiserver is running. So, it is required to have a connection to the Kubernetes cluster where the metal-apiserver is running.

For partition deployments we recommend to just provide a deployment token issued by hand and store this token in the deployment variables.

All tasks for this are run on the deployment machine (`localhost`). The token is then exported with the name `metal_deployment_admin_token` as an Ansible fact for the `localhost`.

Please note that the created token has admin privileges by nature and expires after 8 hours. It should not be stored on a target host.

## Requirements

- The metal-stack V2 API client needs to be installed (see [metal-v2-client role](../metal-v2-client/))

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                                    | Mandatory | Description                                               |
| --------------------------------------- | --------- | --------------------------------------------------------- |
| metal_deployment_token_secret_name      |           | The secret name in which the admin token gets stored      |
| metal_deployment_token_secret_namespace |           | The secret namespace in which the admin token gets stored |
| metal_deployment_token_secret_key       |           | The secret key under which the admin token gets stored    |
