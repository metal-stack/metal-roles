# Zitadel

Role that deploys and manages and configures [Zitadel](https://zitadel.com/), an open-source identity and access management system.

> [!IMPORTANT]
> This role was introduced as part of the implementation of [MEP-4](https://metal-stack.io/docs/MEP-4-multi-tenancy-for-the-metal-api) and is currently considered as alpha stage. Please do not use this role for production use-cases at the time being.

## UI

Because `ExternalSecure: true` is set by default, Zitadel is only available over HTTPS. Using Zitadel with HTTP does currently not work due to <https://github.com/zitadel/zitadel/issues/11019>.

## Other

- Login image not loading because of csp (<https://github.com/zitadel/zitadel/pull/11088>)
- For deploying data automatically through CI, we use <https://github.com/metal-stack/zitadel-init>

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

This role depends on default values of [metal-roles/control-plane/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/control-plane/roles/defaults).

```yaml
# Password of the initial zitadel admin user.
zitadel_admin_password: Password1!
# Repository URL of the zitadel helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
zitadel_chart_repo: null
# Version of the zitadel helm chart. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
zitadel_chart_version: null
# Address of the zitadel database.
zitadel_db_address: zitadel-db
# Password of the zitadel database.
zitadel_db_password: change-me
# Whether to create an ingress for zitadel.
zitadel_enabled_ingress: true
# The zitadel endpoint host name.
zitadel_endpoint: auth.{{ metal_control_plane_gateway_dns }}
# REQUIRED: The external domain configured for the zitadel instance.
zitadel_external_domain: null
# Whether to expose zitadel through a GatewayAPI HTTPRoute instead of an ingress.
zitadel_httproute_enabled: false
# Parent references for the zitadel HTTPRoute.
zitadel_httproute_parent_refs: []
# Image pull policy for the zitadel containers.
zitadel_image_pull_policy: '{{ metal_control_plane_image_pull_policy }}'
# Image tag of zitadel. Uses the chart default when unset.
zitadel_image_tag: null
# Additional annotations for the zitadel ingress.
zitadel_ingress_annotations: {}
# The external URL of the zitadel ingress.
zitadel_ingress_dns: https://auth.{{ metal_control_plane_gateway_dns }}:443
# Configuration for the zitadel-metal-init job (static users, project, application, generic OIDC providers).
zitadel_init_config: {}
# Image name of the zitadel-metal-init job. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
zitadel_init_image_name: null
# Image tag of the zitadel-metal-init job. Resolved from the metal-stack release vector via setup_yaml when not set explicitly.
zitadel_init_image_tag: null
# Name of the initial zitadel instance.
zitadel_initial_instance: metal-stack
# Name of the initial zitadel organization.
zitadel_initial_org: metal-stack
# Whether zitadel runs in insecure (http) mode.
zitadel_insecure: false
# The zitadel master key (32 characters).
zitadel_master_key: x123456789012345678901234567891y
# The namespace to deploy zitadel to.
zitadel_namespace: '{{ metal_control_plane_namespace }}'
# The port of the zitadel service.
zitadel_port: 443
# Whether the init job skips TLS certificate verification.
zitadel_skip_verify_tls: false
# Whether TLS is enabled on the zitadel ingress.
zitadel_tls_enabled: true
# Image tag of the kubectl image used by the init job.
zitadel_tools_kubectl_tag: 1.35.1
```
