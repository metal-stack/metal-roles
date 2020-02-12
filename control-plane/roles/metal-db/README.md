# metal-db

This role provides a database for the metal-api that can be used for storing the main application data.

This role just wraps the [rethinkdb-backup-restore](/control-plane/roles/rethinkdb-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `metal_db_` instead of `rethinkdb_`.
