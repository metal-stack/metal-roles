# auditing-meili

This role provides a database for the metal-api that can be used for storing audit traces. The auditing feature has to be explicitly enabled in the metal-api in order to make use of this database.

This role just wraps the [meili-backup-restore](/control-plane/roles/meili-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `auditing_meili_` instead of `meilisearch_`.
