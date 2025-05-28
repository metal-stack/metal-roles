# defaults

Specifies common defaults for the metal-stack deployment.

It also contains the mapping of our [release vector](https://github.com/metal-stack/releases) to Ansible variables using the [setup_yaml](https://github.com/metal-stack/ansible-common/blob/master/library/setup_yaml.py) module.

## Variables

There are global defaults for all roles of this project defined [here](defaults/main.yaml).

| Name                         | Mandatory | Description                               |
| ---------------------------- | --------- | ----------------------------------------- |
| metal_registry_auth_enabled  |           | Enables deployment of image pull secrets  |
| metal_registry_auth_user     |           | The default auth user for the registry    |
| metal_registry_auth_password |           | The password for the user of the registry |
