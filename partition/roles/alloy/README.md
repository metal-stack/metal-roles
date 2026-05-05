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

### `journal-logs` vs `syslog-logs`

On a modern systemd host, journald is a superset of syslog. `/var/log/syslog` is written by rsyslog consuming from journald — it is a filtered, text-rendered subset of the journal. Enabling both snippets on the same host will ship most messages twice and produce duplicates in Loki.

**Pick one based on what the host runs:**

- Use `journal-logs` on hosts with systemd/journald (standard Debian/Ubuntu partition nodes and management servers). It covers everything syslog would, plus systemd unit stdout/stderr.
- Use `syslog-logs` on hosts without journald (some minimal switch OS images), or where rsyslog applies custom filtering that makes `/var/log/syslog` meaningfully different from the raw journal.

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

## Variables

| Name                  | Mandatory | Description                                                                  |
| --------------------- | --------- | ---------------------------------------------------------------------------- |
| alloy_config_host_dir   |           | The location of the alloy config on the host (default: `/etc/alloy`)         |
| alloy_image_name        | yes       | Image name of alloy                                                          |
| alloy_image_tag         | yes       | Image tag of alloy                                                           |
| alloy_loki_write_endpoints | yes       | List of Loki push endpoints. Each entry: `{url, basic_auth?: {username, password}}` |
| alloy_docker_log_driver |           | Docker log driver for the alloy container (default: `json-file`)             |
| alloy_config_snippets   |           | List of snippet names to enable (default: `[alloy-self]`)  |
| alloy_port              |           | Port for Alloy metrics and HTTP API (default: `12345`)                        |
| alloy_config_raw        |           | Full Alloy River config as a string. When set, bypasses snippet assembly entirely — `alloy_loki_write_endpoints` and `alloy_config_snippets` are ignored. |

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
3. If you have a custom promtail scrape config, convert it once with the [`alloy convert`](https://grafana.com/docs/alloy/latest/reference/cli/convert/) CLI (`--source-format=promtail`) and add the result as a new snippet under `templates/snippets/`, then enable it via `alloy_config_snippets`. Be aware of the [converter limitations](https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/#limitations) — not all promtail features are supported, and the output should always be reviewed manually before use.

   You can run the converter without installing Alloy locally using Docker:

   ```bash
   docker run \
     -v ./promtail.yaml:/etc/promtail/promtail.yaml \
     -v ./config.alloy:/etc/alloy/config.alloy \
     grafana/alloy:latest \
       convert --source-format=promtail --output=/etc/alloy/config.alloy /etc/promtail/promtail.yaml
   ```

   Note: the input must be a fully rendered promtail config (no Ansible variables). Substitute real values before running the converter. After conversion, review the output and replace any hardcoded host-specific values (hostnames, partition IDs, URLs, credentials) with Ansible variables (e.g. `{{ inventory_hostname }}`, `{{ metal_partition_id }}`) so the snippet works correctly across all target hosts.

   If the snippet system does not provide enough flexibility, you can bypass it entirely by setting `alloy_config_raw` to a full Alloy River config string. Ansible variables (e.g. `{{ inventory_hostname }}`) can be used inside the string and will be resolved at deploy time. See the `alloy_config_raw` entry in the Variables table above.

4. Update Prometheus inventory: rename `prometheus_promtail_targets` → `prometheus_alloy_targets` (port `12345` instead of `9080`).
5. If your environment deploys Alloy on different host groups with different scrape needs (e.g. leaf switches vs. management servers), set `alloy_config_snippets` in per-group inventory files rather than at the partition level:

   ```
   group_vars/leaves/alloy.yaml       ← alloy_config_snippets: [leaf-node-docker, alloy-self, syslog-logs]
   group_vars/mgmtservers/alloy.yaml  ← alloy_config_snippets: [alloy-self, journal-logs]
   group_vars/partition/alloy.yaml    ← alloy_loki_write_endpoints: [...] (shared by all)
   ```

6. Once the Alloy deployment is verified (logs arriving in Loki with correct labels), remove the old promtail container and config from the hosts:

   ```bash
   docker rm -f promtail
   rm -rf /etc/promtail
   ```

   Keep the `promtail` role available in your playbook until all environments have been migrated.

### WAL and positions file persistence

Alloy stores its write-ahead log (WAL) — including cursor state for `loki.source.file` and `loki.source.journal` — under `--storage.path`, which is set to `/var/lib/alloy` (bind-mounted from the host). This survives container restarts, preventing duplicate log shipments.

The `syslog-logs` snippet sets `legacy_positions_file = "/var/log/promtail-positions.yaml"`. On first start after migration, Alloy reads the existing promtail positions file and continues tailing `/var/log/syslog` from where promtail left off. No log lines are re-shipped.

`loki.source.journal` has no equivalent migration path — its cursor is WAL-only. The very first Alloy start after migration will re-read a portion of the journal (however much the kernel still has buffered, typically a few thousand lines). This is a one-time event and subsequent restarts are safe once the WAL is populated.

Once the promtail role has been removed from all hosts, the `legacy_positions_file` line can be dropped from the snippet and the old `/var/log/promtail-positions.yaml` file cleaned up from hosts.
