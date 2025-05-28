# defaults

Specifies common defaults for the metal-stack deployment.

## Variables

There are global defaults for all roles of this project defined [here](defaults/main.yaml).

| Name                         | Mandatory | Description                               |
| ---------------------------- | --------- | ----------------------------------------- |
| metal_registry_auth_enabled  |           | Enables deployment of image pull secrets  |
| metal_registry_auth_user     |           | The default auth user for the registry    |
| metal_registry_auth_password |           | The password for the user of the registry |
