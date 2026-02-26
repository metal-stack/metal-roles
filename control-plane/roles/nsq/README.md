# nsq

Deploys [nsq](https://nsq.io/) in a standalone configuration.

The admin console can be reached by using port-forwarding:

```bash
kubectl port-forward -n metal-control-plane svc/nsqadmin 4171
```

Adding nsqadmin as a sidecar into the nsqd pod was the only reasonable way to make the admin console work properly in this setup. This is because we enforce certificate authentication via the TCP port but do not use encrypted communication for in-cluster traffic via the HTTP endpoints, which nsadmin does not really like.

## Variables

This role uses variables from [control-plane-defaults](/control-plane/roles/defaults/defaults/main.yaml). So, make sure you define them adequately as well.

You can look up all the default values of this role in the [defaults folder](defaults/main.yaml).

| Name                           | Mandatory | Description                                                                                 |
| ------------------------------ | --------- | ------------------------------------------------------------------------------------------- |
| nsq_image_name                 | yes       | Image name of nsq                                                                           |
| nsq_image_tag                  | yes       | Image version of nsq                                                                        |
| nsq_namespace                  |           | The deployment's target namespace                                                           |
| nsq_set_resource_limits        |           | Deploys nsq with or without resource limits (possibly disable for development environments) |
| nsq_nsqd_resources             |           | The kubernetes resources for the actual nsqd container                                      |
| nsq_nsq_admin_resources        |           | The kubernetes resources for the actual nsq admin container                                 |
| nsq_nsq_lookupd_resources      |           | The kubernetes resources for the actual nsq lookupd container                               |
| nsq_log_level                  |           | The nsq log level                                                                           |
| nsq_broadcast_address          |           | The nsq broadcast address                                                                   |
| nsq_nsqd_data_size             |           | The size of the nsqd data volume (used when memory cache is full)                           |
| nsq_tls_enabled                |           | Enables TLS for nsq                                                                         |
| nsq_tls_require                |           | Specifies whether TLS is required for client connections (`true`, `false`, or `tcp-https`). |
| nsq_certs_client_key           |           | The nsq certificate client key as a string                                                  |
| nsq_certs_client_cert          |           | The nsq client certificate as a string                                                      |
| nsq_certs_ca_cert              |           | The nsq ca certificate as a string                                                          |
| nsq_image_pull_policy          |           | Image pull policy (defaults to IfNotPresent)                                                |
| nsq_enable_security_context    |           | Enables SecurityContext for the nsq StatefulSet and containers                              |
| nsq_sts_security_context       |           | The SecurityContext for the StatefulSet                                                     |
| nsq_container_security_context |           | The SecurityContext for the Containers                                                      |
