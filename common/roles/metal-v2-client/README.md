# metal-v2-client

Sets up [metal-stack-api](https://pypi.org/project/metal-stack-api/) client library from [api](https://github.com/metal-stack/api).

By default, this role uses the release vector to derive the fitting version of the client library.

## Variables

```yaml
# Install the client from the git repository instead of PyPI.
metal_v2_client_install_from_git_repository: false
# Install the latest available client as fallback when the requested version is not available.
metal_v2_client_install_latest_on_version_error: true
```
