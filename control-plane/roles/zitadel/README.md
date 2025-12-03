# Zitadel

Role that deploys and manages and configures [Zitadel](https://zitadel.com/), an open-source identity and access management system.

> [!IMPORTANT]
> This role was introduced as part of the implementation of [MEP-4]() and is currently considered as alpha stage. Please do not use this role for production use-cases at the time being.

## UI

Because `ExternalSecure: true` is set by default, Zitadel is only available over HTTPS. Using Zitadel with HTTP does currently not work due to https://github.com/zitadel/zitadel/issues/11019.

## Other

- Login image not loading because of csp (https://github.com/zitadel/zitadel/pull/11088)
