# netapp-security-accounts

Creates local, password-authenticated accounts through the NetApp ONTAP REST API. All API calls run once on the Ansible control node, and tasks containing credentials or account passwords use `no_log`.

The role uses `GET /api/security/accounts` to check whether an account exists and `POST /api/security/accounts` to create a missing account. The endpoint is available in ONTAP 9.6 and newer. See the [NetApp security accounts API documentation](https://docs.netapp.com/us-en/ontap-restapi/post-security-accounts.html) for the request schema and supported combinations of applications and authentication methods.

Existing accounts are left unchanged. ONTAP does not return account passwords, so the role cannot compare a configured password with the current password. Change an existing password explicitly outside this role instead of rotating it on every Ansible run.

## Variables

| Name                                      | Mandatory | Description                                                                      |
| ----------------------------------------- | --------- | -------------------------------------------------------------------------------- |
| netapp_security_accounts_host             | yes       | ONTAP cluster management IP address or DNS name                                  |
| netapp_security_accounts_username         | yes       | ONTAP account used for REST API authentication                                   |
| netapp_security_accounts_password         | yes       | Password used for REST API authentication                                        |
| netapp_security_accounts                  |           | Security account request bodies; defaults to an empty list                       |
| netapp_security_accounts_port             |           | ONTAP REST API HTTPS port; defaults to `443`                                     |
| netapp_security_accounts_api_url          |           | REST API base URL derived from the host and port                                 |
| netapp_security_accounts_validate_certs   |           | Validate the ONTAP HTTPS certificate; defaults to `true`                         |
| netapp_security_accounts_timeout          |           | REST request timeout in seconds; defaults to `30`                                |
| netapp_security_accounts_use_proxy        |           | Use proxy settings from the control-node environment; defaults to `false`        |

Each account requires `name`, `password`, and a non-empty `applications` list containing the `password` authentication method. Optional fields supported by the role are `owner`, `role`, `comment`, `locked`, and `password_hash_algorithm`. Omit `owner` for a cluster-scoped account; provide `owner.name` or `owner.uuid` for an SVM-scoped account.

Store both the administrative password and new account passwords in Ansible Vault or another secret store.

## Example

```yaml
- name: Create an ONTAP REST account
  ansible.builtin.include_role:
    name: metal-roles/control-plane/roles/netapp-security-accounts
  vars:
    netapp_security_accounts_host: 192.0.2.10
    netapp_security_accounts_username: admin
    netapp_security_accounts_password: "{{ vault_netapp_admin_password }}"
    netapp_security_accounts:
      - name: gardener
        password: "{{ vault_netapp_gardener_password }}"
        applications:
          - application: http
            authentication_methods:
              - password
        role:
          name: readonly
        comment: Gardener ONTAP integration
```
