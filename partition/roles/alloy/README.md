# alloy

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) in a systemd-managed Docker container.

This role replaces the `promtail` role. Alloy is configured to forward logs to Loki and exposes its own metrics endpoint for scraping by Prometheus.

## Configuration layout

The Alloy configuration is assembled from a base template plus a list of opt-in snippets:

- `templates/config.alloy.j2` — base config, always rendered. Defines the shared `loki.write "default"` endpoint.
- `templates/snippets/<name>.alloy.j2` — opt-in snippets, enabled via `alloy_config_snippets`.

At deploy time each enabled snippet is rendered into `{{ alloy_config_host_dir }}/conf.d/` and concatenated into a single `config.alloy` file.

Available snippets:

| Snippet            | Description                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------ |
| `alloy-self`       | Meta-monitoring: forwards Alloy's own logs to Loki with `job=alloy` and `node_name` labels |
| `leaf-node-docker` | Scrapes Docker container logs on the host and forwards them to Loki                        |
| `journal-logs`     | Scrapes the systemd journal and forwards to Loki; relabels `unit` from `__journal__systemd_unit` |
| `syslog-logs`      | Tails `/var/log/syslog` and forwards to Loki with `job=syslog`, `partition`, and `host` labels |

## Adding custom snippets

You can extend the Alloy config with your own snippets without modifying this role.

1. Create a Jinja2 template that renders valid [Alloy River syntax](https://grafana.com/docs/alloy/latest/reference/config-blocks/) in your own role or playbook files directory, e.g. `templates/snippets/my-custom.alloy.j2`.
2. Add it to your tasks before this role runs, or use [`ansible.builtin.template`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html) to render it directly into `{{ alloy_config_host_dir }}/conf.d/` on the target host with a filename starting with `60-` or higher so it sorts after the built-in snippets.
3. Alternatively, add the template to this role's `templates/snippets/` and reference it in `alloy_config_snippets`:

   ```yaml
   alloy_config_snippets:
     - alloy-self
     - leaf-node-docker
     - my-custom
   ```

   A snippet template can use any Ansible variables available on the host. It must not define `loki.write "default"` (already in the base config) but can freely reference `loki.write.default.receiver` as a forwarding target.



| Name                  | Mandatory | Description                                                                  |
| --------------------- | --------- | ---------------------------------------------------------------------------- |
| alloy_config_host_dir   |           | The location of the alloy config on the host (default: `/etc/alloy`)         |
| alloy_image_name        | yes       | Image name of alloy                                                          |
| alloy_image_tag         | yes       | Image tag of alloy                                                           |
| alloy_loki_write_endpoints | yes       | List of Loki push endpoints. Each entry: `{url, basic_auth?: {username, password}}` |
| alloy_docker_log_driver |           | Docker log driver for the alloy container (default: `json-file`)             |
| alloy_config_snippets   |           | List of snippet names to enable (default: `[alloy-self]`)  |
| alloy_port              |           | Port for Alloy metrics and HTTP API (default: `12345`)                        |

## Meta-monitoring

Alloy exposes its own Prometheus metrics on `0.0.0.0:12345/metrics` (configured via the systemd container command). Add the host targets to `prometheus_alloy_targets` in the prometheus role to scrape them.

Alloy's own logs are forwarded to Loki when the `alloy-self` snippet is enabled.

## Migration from `promtail`

This role supersedes the `promtail` role. To migrate:

1. Replace the `promtail` role with `alloy` in your playbook (e.g. `deploy_partition.yaml`).
2. Remove the old `promtail_clients` / `promtail_scrape_configs` variables from your inventory. Set `alloy_loki_write_endpoints` to the Loki push endpoint(s) instead, e.g.:

   ```yaml
   alloy_loki_write_endpoints:
     - url: "http://loki.{{ metal_control_plane_ingress_dns }}:8080/loki/api/v1/push"
   ```
3. If you have a custom promtail scrape config, convert it once with the [`alloy convert`](https://grafana.com/docs/alloy/latest/reference/cli/convert/) CLI (`--source-format=promtail`) and add the result as a new snippet under `templates/snippets/`, then enable it via `alloy_config_snippets`.
4. Update Prometheus inventory: rename `prometheus_promtail_targets` → `prometheus_alloy_targets` (port `12345` instead of `9080`).
5. Remove the old promtail container/config from the hosts (`docker rm -f promtail` and `rm -rf /etc/promtail`).
