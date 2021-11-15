# metal-python

Sets up [metal-python](https://github.com/metal-stack/metal-python).

The fitting version of metal-python corresponds to the metal-api release version.

## Requirements

None

## Variables

| Name                                         | Mandatory | Description                                                                  |
| -------------------------------------------- | --------- | ---------------------------------------------------------------------------- |
| metal_python_version                         | yes       | The metal-python version to install.                                         |
| metal_python_fallback_to_metal_api_version   |           | Attempts to derive fitting metal-python version from release vector          |
| metal_python_install_latest_on_version_error |           | Whether to just install latest metal-python when given version was not found |

## Examples

```
- name: Install metal-python
  include_role:
    name: metal-roles/control-plane/roles/metal-python
  vars:
    metal_python_version: "{{ metal_api_image_tag }}"
```
