# zitadel-db

This role provides a database for the zitadel oidc-provider.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `zitadel_db_` instead of `postgres_`.
