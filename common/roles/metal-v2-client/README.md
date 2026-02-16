# metal-v2-client

Sets up [metal-stack-api](https://pypi.org/project/metal-stack-api/) client library from [api](https://github.com/metal-stack/api).

By default, this role uses the release vector to derive the fitting version of the client library.

## Requirements

None

## Variables

| Name                                            | Mandatory | Description                                                                               |
| ----------------------------------------------- | --------- | ----------------------------------------------------------------------------------------- |
| metal_v2_client_install_latest_on_version_error |           | Whether to just install latest client library version when given version was not found    |
| metal_v2_client_install_from_git_repository     |           | Alternatively, install directly from the git repository (e.g. for testing a devel branch) |
