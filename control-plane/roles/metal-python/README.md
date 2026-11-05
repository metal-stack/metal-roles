# metal-python

Sets up [metal-python](https://github.com/metal-stack/metal-python).

By default, this role uses the release vector to derive the fitting version of metal-python.

## Variables

This role depends on default values of [metal-roles/common/roles/defaults](https://github.com/metal-stack/tree/master/metal-roles/common/roles/defaults).

```yaml
# Install the client from the git repository instead of PyPI.
metal_python_install_from_git_repository: false
# Install the latest available client as fallback when the requested version is not available.
metal_python_install_latest_on_version_error: true
# The metal-python version to install. Required unless metal_python_version_from_release_vector is true.
metal_python_version: null
# Derive the metal-python version from the metal-stack release vector.
metal_python_version_from_release_vector: true
```
