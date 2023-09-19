# auditing-meili

This role deploys a helm chart for [MeiliSearch](https://github.com/meilisearch/meilisearch-kubernetes) for auditing purposes.

This role just wraps the [meili-backup-restore](/control-plane/roles/meili-backup-restore) role. Refer to this role for further documentation.

## Variables

The role should take the same variables as the wrapped role, but prefixed with `auditing_meili_` instead of `meilisearch_`.
