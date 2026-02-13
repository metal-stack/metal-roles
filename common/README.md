# common

Contains common roles for deploying the metal-stack.

## Roles

| Role Name                                              | Description                                                                                                                |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| [defaults](roles/defaults)                             | Provides defaults both relevant for partition and control-plane, it also provides a release vector mapping for metal-roles |
| [metal-deployment-token](roles/metal-deployment-token) | Creates an V2 admin token that can be used during the deployment to create API resources                                   |
| [metal-v2-client](roles/metal-v2-client)               | Installs metal-stack-api                                                                                                   |
