# nsq

Deploys [nsq](https://nsq.io/) in a standalone configuration.

The admin console can be reached by using port-forwarding:

```bash
kubectl port-forward -n metal-control-plane svc/nsqadmin 4171
```

Adding nsqadmin as a sidecar into the nsqd pod was the only reasonable way to make the admin console work properly in this setup. This is because we enforce certificate authentication via the TCP port but do not use encrypted communication for in-cluster traffic via the HTTP endpoints, which nsadmin does not really like.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](../../../common/roles/defaults/README.md).

This role depends on default values of [metal-roles/control-plane/roles/defaults](../defaults/README.md).

```yaml
# The address nsqd broadcasts to consumers.
nsq_broadcast_address: '{{ metal_control_plane_gateway_dns }}'
# The nsq CA certificate content.
nsq_certs_ca_cert: null
# The nsq client certificate content.
nsq_certs_client_cert: null
# The nsq client certificate key content.
nsq_certs_client_key: null
# Security context for the containers.
nsq_container_security_context:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
# Whether to render the pod and container security contexts.
nsq_enable_security_context: false
# Image name of nsq. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
nsq_image_name: null
# Image pull policy for the nsq containers.
nsq_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of nsq. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
nsq_image_tag: null
# Log level of the nsq components.
nsq_log_level: info
# The namespace to deploy nsq to.
nsq_namespace: '{{ metal_control_plane_namespace }}'
# Resource requests and limits for the nsq-admin container.
nsq_nsq_admin_resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 30m
    memory: 32Mi
# Resource requests and limits for the nsq-lookupd container.
nsq_nsq_lookupd_resources:
  limits:
    cpu: '1'
    memory: 100Mi
  requests:
    cpu: 20m
    memory: 8Mi
# Size of the nsqd data volume.
nsq_nsqd_data_size: 100Mi
# Resource requests and limits for the nsqd container.
nsq_nsqd_resources:
  limits:
    cpu: '1'
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 32Mi
# Docker auth configuration for the image pull secret.
nsq_registry_auth:
  auths:
    '{{ metal_registry_url }}':
      auth: '{{ (metal_registry_auth_user + '':'' + metal_registry_auth_password) | b64encode }}'
      password: '{{ metal_registry_auth_password }}'
      username: '{{ metal_registry_auth_user }}'
# Whether to deploy an image pull secret for the registry.
nsq_registry_auth_enabled: '{{ metal_registry_auth_enabled }}'
# Whether to set resource requests and limits on the nsq containers.
nsq_set_resource_limits: true
# Pod security context for the statefulset.
nsq_sts_security_context:
  fsGroup: 2000
  fsGroupChangePolicy: OnRootMismatch
  runAsGroup: 2000
  runAsNonRoot: true
  runAsUser: 1001
  seccompProfile:
    type: RuntimeDefault
# Whether to expose nsqd through a GatewayAPI TCPRoute instead of an ingress.
nsq_tcproute_enabled: false
# Parent references for the nsqd TCPRoute.
nsq_tcproute_parent_refs: []
# Whether TLS is enabled for nsqd.
nsq_tls_enabled: false
# The nsqd tls-required setting.
nsq_tls_require: tcp-https
```
