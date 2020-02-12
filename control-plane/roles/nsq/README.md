# nsq

Deploys [nsq](https://nsq.io/) in a standalone configuration.

The admin console can be reached by using port-forwarding:

```
kubectl port-forward -n metal-control-plane svc/nsqadmin 4171
```

Adding nsqadmin as a sidecar into the nsqd pod was the only reasonable way to make the admin console work properly in this setup. This is because we enforce certificate authentication via the TCP port but do not use encrypted communication for in-cluster traffic via the HTTP endpoints, which nsadmin does not really like.

As our control plane also requires non-HTTP ports to be exposed to the outside world, we currently use [tcp and udp service exposal of Kubernetes nginx-ingress](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/).

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                             | Mandatory | Description                                                                                                                        |
| -------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| nsq_image_name                   |           | Image name of nsq                                                                                                                  |
| nsq_image_tag                    |           | Image version of nsq                                                                                                               |
| nsq_expose_ingress_service_ports |           | Exposes tcp and udp services over nginx-ingress, requires [nginx-ingress](https://github.com/kubernetes/ingress-nginx) to be setup |
| nsq_set_resource_limits          |           | Deploys nsq with or without resource limits (possibly disable for development environments)                                        |
| nsq_nsqd_resources               |           | The kubernetes resources for the actual nsqd container                                                                             |
| nsq_nsq_lookupd_resources        |           | The kubernetes resources for the actual nsq lookupd container                                                                      |
| nsq_log_level                    |           | The nsq log level                                                                                                                  |
| nsq_broadcast_address            |           | The nsq broadcast address                                                                                                          |
| nsq_nsqd_data_size               |           | The size of the nsqd data volume (used when memory cache is full)                                                                  |
| nsq_tls_enabled                  |           | Enables TLS for nsq                                                                                                                |
| nsq_certs_client_key             |           | The nsq certifate client key as a string                                                                                           |
| nsq_certs_client_cert            |           | The nsq client certificate as a string                                                                                             |
| nsq_certs_ca_cert                |           | The nsq ca certificate as a string                                                                                                 |
