# auditing-meili

This role deploys a helm chart for [MeiliSearch](https://github.com/meilisearch/meilisearch-kubernetes) for auditing purposes.

## Variables

| Name                             | Mandatory | Description                                                                                    |
| -------------------------------- | --------- | ---------------------------------------------------------------------------------------------- |
| metal_auditing_meili_secret      |           | The content of the auth secret. If empty or not provided, the secret must be created manually. |
| metal_auditing_meili_ingress     |           | Configuratrion for ingress, check example or helm chart for details                            |
| metal_auditing_meili_persistence |           | Configuration for persistence, check example or helm chart for details                         |
| metal_auditing_meili_environment |           | Sets Meilisearch environment to development/production                                         |
