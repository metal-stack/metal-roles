# Zitadel

Role that deploys and manages and configures [Zitadel](https://zitadel.com/), an open-source identity and access management system.

## UI

Because `ExternalSecure: true` is set by default, Zitadel is only available over HTTPS. Using Zitadel with HTTP does currently not work due to <https://github.com/zitadel/zitadel/issues/11019>.

## Other

- Login image not loading because of csp (<https://github.com/zitadel/zitadel/pull/11088>)
- For deploying data automatically through CI, we use <https://github.com/metal-stack/zitadel-init>

## Variables

You can look up all the default values of this role [here](defaults/main.yaml).

| Name                          | Mandatory | Description                                                                                                                     |
| ----------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| zitadel_chart_version         |           | The chart version for deploying zitadel                                                                                         |
| zitadel_namespace             |           | The namespace into which zitadel is deployed                                                                                    |
| zitadel_init_image_name       | yes       | The zitadel-init image tag                                                                                                      |
| zitadel_init_image_tag        | yes       | The zitadel-init image name                                                                                                     |
| zitadel_actions_enabled       |           | Whether to deploy the zitadel actions V2 server as a dedicated deployment                                                       |
| zitadel_actions_allow_roles   |           | Roles that must be present in the idp role claims, otherwise login is prevented                                                 |
| zitadel_actions_client_ids    |           | Client ids for which the role policy is enforced; if empty, derived from the client_id in the zitadel-client-credentials secret |
| zitadel_actions_deny_list     |           | Fully operator-controlled HTTPClient.DenyList; by default only localhost is blocked, all IPs allowed                            |
| zitadel_image_tag             |           | An optional image overwrite for zitadel when not using the default from the helm chart                                          |
| zitadel_tools_kubectl_tag     |           | The zitadel tools kubectl image tag (of alpine/k8s)                                                                             |
| zitadel_external_domain       | yes       | The external domain used by zitadel                                                                                             |
| zitadel_image_pull_policy     |           | The image pull policy to use for zitadel-init                                                                                   |
| zitadel_ingress_dns           |           | The DNS ingress domain used for the ingress-controller                                                                          |
| zitadel_ingress_annotations   |           | Annotations for the zitadel ingress resource(s)                                                                                 |
| zitadel_initial_instance      |           | The name of the initial instance                                                                                                |
| zitadel_initial_org           |           | The name of the initial organization                                                                                            |
| zitadel_admin_password        |           | The admin password for the login of the administrator in the UI                                                                 |
| zitadel_master_key            |           | The master key (must be 32 bytes!)                                                                                              |
| zitadel_db_address            |           | The address for the zitadel-db                                                                                                  |
| zitadel_db_password           |           | The password for accessing the zitadel-db                                                                                       |
| zitadel_enabled_ingress       |           | Whether to enable ingress exposal or not                                                                                        |
| zitadel_init_config           |           | Configuration for zitadel-init                                                                                                  |
| zitadel_port                  |           | The port used by zitadel                                                                                                        |
| zitadel_skip_verify_tls       |           | Whether to skip TLS verification for zitadel                                                                                    |
| zitadel_insecure              |           | Whether to allow insecure connections to zitadel                                                                                |
| zitadel_httproute_enabled     |           | Deploys a Gateway API HTTPRoute exposing zitadel via the configured Gateway                                                     |
| zitadel_httproute_parent_refs |           | List of `parentRefs` (Gateways) the HTTPRoute attaches to                                                                       |
