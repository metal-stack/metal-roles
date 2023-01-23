# auditing-meili

This role deploys a helm chart for [MeiliSearch](https://github.com/meilisearch/meilisearch-kubernetes) for auditing purposes. It reuses configurations from the [metal#Auditing](../metal/README.md#auditing) role.

## Variables

| Name                             | Mandatory | Description                                                                                    |
| -------------------------------- | --------- | ---------------------------------------------------------------------------------------------- |
| metal_auditing_meili_secret_name |           | The name of the secret to be used.                                                             |
| metal_auditing_meili_secret      |           | The content of the auth secret. If empty or not provided, the secret must be created manually. |
