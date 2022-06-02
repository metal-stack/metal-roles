# pixiecore

Deploys pixiecore in a systemd-managed Docker container.

## Variables

| Name                              | Mandatory | Description                                                                                                   |
| --------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| pixiecore_image_name              | yes       | Image version of the pixiecore                                                                                |
| pixiecore_image_tag               | yes       | Image tag of the pixiecore                                                                                    |
| pixiecore_api_url                 |           | The url the pixiecore server uses in api mode for requesting the boot image. Should point to metal-core.      |
| pixiecore_dns_servers             |           | Alternative DNS servers to be used by the pixiecore (can be used for configuring kernel and boot image cache) |
| pixiecore_partition_id            |           | The partition where pixiecore is installed                                                                    |
| pixiecore_grpc_cert_dir           |           | The directory where the grpc certificates reside                                                              |
| pixiecore_grpc_ca_cert            | yes       | The filename of the ca certificate                                                                            |
| pixiecore_grpc_client_cert        | yes       | The filename of the client certificate                                                                        |
| pixiecore_grpc_client_key         | yes       | The filename of the client key                                                                                |
| pixiecore_grpc_address            |           | The address of metal-api grpc endpoint in the form (ip or hostname:port)                                      |
| pixiecore_metal_api_url           |           | The URL where to reach metal-api                                                                              |
| pixiecore_metal_api_hmac_view_key |           | A view hmac to authenticate against metal-api (given to the metal-hammer)                                     |
