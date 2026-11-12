# wireguard

Configures a wireguard-server.

## Variables

```yaml
# Directory in which the wireguard keys are stored.
wireguard_cert_directory: /etc/pki/wireguard
# Group of the wireguard key directory.
wireguard_cert_group: root
# Owner of the wireguard key directory.
wireguard_cert_owner: root
# Wireguard clients to configure. Each entry supports name, public_key and client_id.
wireguard_clients: []
# REQUIRED: The wireguard server address (CIDR) configured on the wg0 interface.
wireguard_ip: null
# The port the wireguard server listens on.
wireguard_listen_port: 51820
# Pre-generated wireguard private key. When unset, a key pair is generated on the host.
wireguard_private_key: null
# Pre-generated wireguard public key. When unset, a key pair is generated on the host.
wireguard_public_key: null
```
