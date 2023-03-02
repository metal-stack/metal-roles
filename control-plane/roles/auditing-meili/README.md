# auditing-meili

This role deploys a helm chart for [MeiliSearch](https://github.com/meilisearch/meilisearch-kubernetes) for auditing purposes.

## Variables

| Name                       | Mandatory | Description                                                                                    |
| -------------------------- | --------- | ---------------------------------------------------------------------------------------------- |
| auditing_meili_secret      |           | The content of the auth secret. If empty or not provided, the secret must be created manually. |
| auditing_meili_ingress     |           | Configuratrion for ingress, check example or helm chart for details                            |
| auditing_meili_persistence |           | Configuration for persistence, check example or helm chart for details                         |
| auditing_meili_environment |           | Sets Meilisearch environment to development/production                                         |
| auditing_meili_namespace   |           | Namespace to deploy MeiliSearch                                                                |
