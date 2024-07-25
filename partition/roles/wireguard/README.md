# wireguard

Configures a wireguard-server.

## Variables

| Name                         | Mandatory | Description                                                                                               |
| ---------------------------- | --------- | --------------------------------------------------------------------------------------------------------- |
| wireguard_cert_directory     |           | the directory to store wireguard certs.                                                                   |
| wireguard_cert_owner         |           | the user that should own the cert.                                                                        |
| wireguard_cert_group         |           | the group that should own the cert.                                                                       |
| wireguard_ip                 | yes       | the ip where wireguard should bind to. e.g. (`100.1.2.1/24`)                                              |
| wireguard_listen_port        |           | the port wireguard should listen on (default is 51820)                                                    |
| wireguard_clients            |           | array of clients to be configured at the server side                                                      |
| wireguard_clients.name       | yes       | a speaking name for this client as description.                                                           |
| wireguard_clients.public_key | yes       | the public key that identifies this client.                                                               |
| wireguard_clients.client_id  | yes       | a unique id for this client - is used to automatically generate client IP out of the `wireguard_ip` CIDR. |
| wireguard_clients.client_id  | yes       | a unique id for this client - is used to automatically generate client IP out of the `wireguard_ip` CIDR. |
| wireguard_public_key         |           | optional pre-generated public for wireguard                                                               |
| wireguard_private_key        |           | optional pre-generated private for wireguard                                                              |
