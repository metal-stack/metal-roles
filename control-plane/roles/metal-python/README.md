# metal-python

Sets up [metal-python](https://github.com/metal-stack/metal-python).

By default, this role uses the release vector to derive the fitting version of metal-python.

## Requirements

None

## Variables

| Name                                         | Mandatory | Description                                                                               |
| -------------------------------------------- | --------- | ----------------------------------------------------------------------------------------- |
| metal_python_version                         |           | The specific metal-python version to install.                                             |
| metal_python_version_from_release_vector     |           | Attempts to derive fitting metal-python version from release vector                       |
| metal_python_install_latest_on_version_error |           | Whether to just install latest metal-python when given version was not found              |
| metal_python_install_from_git_repository     |           | Alternatively, install directly from the git repository (e.g. for testing a devel branch) |

## Examples

```
- name: Install metal-python
  include_role:
    name: metal-roles/control-plane/roles/metal-python

- name: Install specific metal-python version
  include_role:
    name: metal-roles/control-plane/roles/metal-python
  vars:
    metal_python_version: "0.10.0"

- name: Install metal-python devel branch
  include_role:
    name: metal-roles/control-plane/roles/metal-python
  vars:
    metal_python_version: "my-nice-feature"
    metal_python_install_from_git_repository: yes
```
