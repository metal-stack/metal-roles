# bmc-proxy

Deploys a bmc-proxy and bmc-reverse-proxy, which is the counterpart to the metal-console running in the metal control plane. This gives users SSH and console access to their allocated machines through the control plane.

## Variables

| Name                         | Mandatory | Description                                                                                                        |
| ---------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| bmc_proxy_image_tag          | yes       | Image version of the bmc-proxy                                                                                     |
| bmc_proxy_image_name         | yes       | Image name of the bmc-proxy                                                                                        |
| bmc_reverse_proxy_image_tag  | yes       | Image version of the bmc-reverse-proxy                                                                             |
| bmc_reverse_proxy_image_name | yes       | Image name of the bmc-reverse-proxy                                                                                |
| bmc_proxy_port               |           | The port on which the bmc-proxy listens                                                                            |
| bmc_reverse_proxy_port       |           | The port on which the bmc-reverse-proxy listens                                                                    |
| bmc_proxy_docker_bridge_ip   |           | Required for communication between bmc-proxy and bmc-reverse-proxy, if not defined will be looked up automatically |
