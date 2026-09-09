# haproxy

Installs and configures a single haproxy on a partition management server. Each
entry of `haproxy_services` renders one frontend and one backend into
`/etc/haproxy/haproxy.cfg`, so one instance can carry the kubernetes api on
6443 (tcp) and https ingress on 443 (http with ssl termination) at the same time.

## Usage

```yaml
haproxy_services:
  - name: k3s_apiserver
    mode: tcp
    port: 6443
    healthcheck: livez
    bind_addresses:
      - "{{ wireguard_ip.split('/')[0] }}"
    backends:
      - name: k3s01
        address: 10.1.1.1
      - name: k3s02
        address: 10.1.1.2
  - name: https_in
    mode: http
    port: 443
    ssl_cert: /etc/haproxy/certs/app.pem
    bind_addresses:
      - "{{ wireguard_ip.split('/')[0] }}"
    backends:
      - name: traefik
        address: 10.1.1.1
        port: 30443
```

Frontends are rendered as `fe_<name>`, backends as `be_<name>`.

## Variables

| Name                   | Mandatory | Description                                                                  |
|------------------------|-----------|------------------------------------------------------------------------------|
| haproxy_services       | x         | The services to expose, see the table below.                                 |
| haproxy_backend_port   |           | The backend port a service falls back to, default `6443`.                    |
| haproxy_stats_socket   |           | The stats socket path.                                                       |
| haproxy_timeout_tunnel |           | The client and server timeout, default `4h`.                                 |
| haproxy_check_interval |           | The health check interval, default `2s`.                                     |
| haproxy_check_fall     |           | The failed checks it takes to mark a backend down, default `3`.              |
| haproxy_check_rise     |           | The passed checks it takes to mark a backend up, default `2`.                |
| haproxy_healthchecks   |           | The health checks this role implements. A service may only ask for these.    |
| haproxy_nonlocal_bind  |           | Set `net.ipv4.ip_nonlocal_bind`, default `true`. See below.                  |

Per service:

| Key            | Mandatory | Description                                                                       |
|----------------|-----------|-----------------------------------------------------------------------------------|
| name           | x         | The frontend and backend name.                                                    |
| port           | x         | The port the frontend binds.                                                      |
| bind_addresses | x         | The addresses the frontend binds, one `bind` line each.                           |
| backends       | x         | The servers, each `{name, address, port?}`.                                       |
| mode           |           | `tcp` or `http`, default `tcp`.                                                   |
| backend_port   |           | The port the backends of this service default to.                                 |
| ssl_cert       |           | The pem bundle for ssl termination, `http` mode only. Must already be on the host.|
| healthcheck    |           | `livez`, see below. Without it the backends get a plain tcp connect check.        |
