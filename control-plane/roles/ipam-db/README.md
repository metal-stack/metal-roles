# ipam-db

This role provides a database for the metal-api that can be used for storing ipam data.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `ipam_db_` instead of `postgres_`.
