# auditing-timescaledb

This role provides a database for the metal-api that can be used for storing audit traces. The auditing feature has to be explicitly enabled in the metal-api in order to make use of this database.

This role just wraps the [postgres-backup-restore](/control-plane/roles/postgres-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `auditing_timescaledb_` instead of `postgres_`.
