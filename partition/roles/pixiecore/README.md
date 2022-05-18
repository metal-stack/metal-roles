# pixiecore

Deploys pixiecore in a systemd-managed Docker container.

## Variables

| Name                              | Mandatory | Description                                                                                                   |
|-----------------------------------|-----------|---------------------------------------------------------------------------------------------------------------|
| pixiecore_image_name              | yes       | Image version of the pixiecore                                                                                |
| pixiecore_image_tag               | yes       | Image tag of the pixiecore                                                                                    |
| pixiecore_api_url                 |           | The url the pixiecore server uses in api mode for requesting the boot image. Should point to metal-core.      |
| pixiecore_dns_servers             |           | Alternative DNS servers to be used by the pixiecore (can be used for configuring kernel and boot image cache) |
| pixiecore_partition_id            | yes       | The partition where pixie is installed                                                                        |
| pixiecore_dns_servers             |           | A list of dns servers to use                                                                                  |
| pixiecore_grpc_cert_dir           | yes       | The directory where the grpc certificates reside                                                              |
| pixiecore_grpc_ca_cert            | yes       | The filename of the ca certificate                                                                            |
| pixiecore_grpc_client_cert        | yes       | The filename of the client certificate                                                                        |
| pixiecore_grpc_client_key         | yes       | The filename of the client key                                                                                |
| pixiecore_grpc_address            | yes       | The address of metal-api grpc endpoint in the form (ip or hostname:port)                                      |
| pixiecore_metal_api_url           | yes       | The URL where to reach metal-api                                                                              |
| pixiecore_metal_api_hmac_view_key | yes       | A view hmac to authenticate against metal-api, metal-hammer use this to call machineget                       |
