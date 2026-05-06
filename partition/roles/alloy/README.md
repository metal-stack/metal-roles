# alloy

Deploys [Grafana Alloy](https://grafana.com/docs/alloy/latest/) in a systemd-managed Docker container.

This role replaces the deprecated `promtail` role. Alloy is configured to forward logs to Loki and exposes its own metrics endpoint for scraping by Prometheus. See [Migration from `promtail`](#migration-from-promtail) for step-by-step migration instructions.

## Configuration

The Alloy configuration is assembled from a base template plus a list of opt-in snippets:

- `templates/config.alloy.j2` — base config, always rendered. Defines the shared `loki.write "default"` endpoint.
- `templates/snippets/<name>.alloy.j2` — opt-in snippets, enabled via `alloy_config_snippets`.

At deploy time each enabled snippet is rendered into `{{ alloy_config_host_dir }}/conf.d/` and concatenated into a single `config.alloy` file.

The snippets can be configured with environment variables defined in the [Variables](#variables) section below. This allows you to enable only the features you need without having to maintain a full custom config.

### Available snippets

The snippets are used in our default configs to provide a sensible out-of-the-box setup and can be configured with the variables described in the next section to fit most use cases without modification.

If your needs are more custom (e.g. you have a non-standard log source, or want to use advanced Alloy features not covered by the existing snippets), you can follow the [Customizing the config](#customizing-the-config) section below to either add your own snippet or bypass the snippet system entirely with a custom raw config.

| Snippet            | Description                                                                                                                                                                                                                                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alloy-meta`       | Meta-monitoring: forwards Alloy's own logs to Loki with `job=alloy` and `node_name` labels. Redundant when `journal-logs` is enabled — journald already captures Alloy's stdout/stderr. Log level info and format are always configured via the base config regardless of this snippet.                                               |
| `leaf-node-docker` | Scrapes Docker container logs on the host via the Docker socket and forwards them to Loki. Assumes the `json-file` log driver (the default). If containers use the `journald` log driver instead, their logs are already captured by `journal-logs` — enabling both snippets in that case will produce duplicate log entries in Loki. |
| `journal-logs`     | Scrapes the systemd journal and forwards to Loki; relabels `unit` from `__journal__systemd_unit`. On standard systemd hosts (Debian/Ubuntu), journald captures syslog messages as well, so this snippet typically covers everything `syslog-logs` would. Enabling both may produce duplicate log entries in Loki.                     |
| `syslog-logs`      | Tails `/var/log/syslog` and forwards to Loki with `job=syslog`, `partition`, and `host` labels. Suited for hosts without journald (e.g. minimal switch OS images). On standard systemd hosts, prefer `journal-logs` — enabling both may produce duplicate log entries in Loki.                                                        |

### Variables

| Name                          | Mandatory | Description                                                                                                                                               |
| ----------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| alloy_config_host_dir         |           | The location of the alloy config on the host (default: `/etc/alloy`)                                                                                      |
| alloy_image_name              | yes       | Image name of alloy                                                                                                                                       |
| alloy_image_tag               | yes       | Image tag of alloy                                                                                                                                        |
| alloy_loki_write_endpoints    | yes       | List of Loki push endpoints. Each entry: `{url, remote_timeout?: <duration>, basic_auth?: {username, password}}`                                          |
| alloy_docker_log_driver       |           | Docker log driver for the alloy container (default: `json-file`)                                                                                          |
| alloy_config_snippets         |           | List of snippet names to enable (default: `[]`)                                                                                                           |
| alloy_port                    |           | Port for Alloy metrics and HTTP API (default: `12345`)                                                                                                    |
| alloy_promtail_positions_file |           | Path to the legacy promtail positions file (default: `/var/log/promtail-positions.yaml`). Used by `syslog-logs` on first start after migration.           |
| alloy_config_raw              |           | Full Alloy River config as a string. When set, bypasses snippet assembly entirely — `alloy_loki_write_endpoints` and `alloy_config_snippets` are ignored. |

### Meta-monitoring (for Alloy itself)

#### Metrics

Alloy always exposes Prometheus metrics on `0.0.0.0:{{ alloy_port }}/metrics`, regardless of which snippets are enabled. Add the host targets to `prometheus_alloy_targets` in the prometheus role to scrape them.

#### Logs

Alloy's own logs are captured in two ways depending on your snippet configuration:

- **If `journal-logs` is enabled** — Alloy runs as a systemd-managed Docker container, so its stdout/stderr are captured by journald automatically. No additional snippet is needed.
- **If `journal-logs` is not enabled** (e.g. you only use `syslog-logs` or no log snippet at all) — enable the `alloy-meta` snippet to forward Alloy's own logs to Loki explicitly.

Alloy's log level (`info`) and format (`logfmt`) are always configured via the base config, regardless of which snippets are enabled. The `alloy-meta` snippet only adds the Loki forwarding pipeline on top.

### WAL and positions file persistence

Alloy stores its write-ahead log (WAL) — including cursor state for `loki.source.file` and `loki.source.journal` — under `--storage.path`, which is set to `/var/lib/alloy` (bind-mounted from the host). This survives container restarts, preventing duplicate log shipments.

The `syslog-logs` snippet reads the legacy promtail positions file on first start after migration to continue tailing `/var/log/syslog` from where promtail left off. The path is configured via `alloy_promtail_positions_file` (default: `/var/log/promtail-positions.yaml`). No log lines are re-shipped. This only happens once — after the initial migration, Alloy updates the positions in its own WAL format.

`loki.source.journal` has no equivalent migration path — its cursor is WAL-only. The very first Alloy start after migration will re-read a portion of the journal. This is a one-time event and subsequent restarts are safe once the WAL is populated.

Once the migration is complete, the `legacy_positions_file` line can optionally be dropped from the snippet and the old positions file cleaned up from hosts — Alloy will simply start tracking positions in its own WAL format from that point.

## Customizing the config

There is no way to inject a custom snippet purely from inventory. Your options are:

**Option A — Use `alloy_config_raw`** (inventory only, no role change)

Set `alloy_config_raw` to a full Alloy River config string in your inventory. The role will write it verbatim and skip snippet assembly entirely. `alloy_loki_write_endpoints` and `alloy_config_snippets` are ignored. You own the complete config, including the base `loki.write "default"` block.

**Option B — Add the snippet to this role** (requires editing this repo)

Add the template to `templates/snippets/` and reference it by name in `alloy_config_snippets`:

```yaml
alloy_config_snippets:
  - alloy-meta
  - leaf-node-docker
```

A snippet template can use any Ansible variables available on the host. It does not need to define `loki.write "default"` as it is already in the base config.

Contributions of new snippets are welcome — since all snippets are opt-in via `alloy_config_snippets`, adding one to the role has no impact on existing deployments.

## Migration from `promtail`

Alloy allows reproducing the same log forwarding behavior as promtail via the [available snippets](#available-snippets), but it is a different tool with a different internal data model. Label names, pipeline stages, and how metrics are exposed might differ from promtail. **Review your existing Loki dashboards and alerting rules after the migration and adapt them where necessary.**

**Recommended approach — parallel run:** Deploy Alloy alongside the existing promtail installation first. Both will ship logs to Loki simultaneously, so expect duplicate log entries during this transition window. Once you have verified that logs arrive in Loki with the correct labels and dashboards show data correctly, remove promtail.

1. **Add the `alloy` role** to your playbook alongside `promtail` for a parallel run, or replace it directly if you prefer a hard cut-over.

2. **Configure the Loki endpoint.** Set `alloy_loki_write_endpoints`:

   ```yaml
   alloy_loki_write_endpoints:
     - url: "http://loki.{{ metal_control_plane_ingress_dns }}:8080/loki/api/v1/push"
       remote_timeout: 10s
       basic_auth:
         username: "promtail"
         password: "test"
   ```

3. **Choose snippets** that match your legacy `promtail_scrape_configs` — see [Available snippets](#available-snippets). If the available snippets are close enough to your old setup, enable the relevant ones and adjust with the provided variables. Otherwise, continue with step 4.

   If your environment deploys Alloy on different host groups with different scrape needs (e.g. leaf switches vs. management servers), set `alloy_config_snippets` in per-group inventory files:

   ```text
   group_vars/leaves/alloy.yaml       ← alloy_config_snippets: [leaf-node-docker, journal-logs]
   group_vars/mgmtservers/alloy.yaml  ← alloy_config_snippets: [journal-logs]
   group_vars/partition/alloy.yaml    ← alloy_loki_write_endpoints: [...] (shared by all)
   ```

4. **Convert custom promtail scrape configs** _(optional — only needed if you extended the promtail setup beyond what the available snippets cover)_. Use the [`alloy convert`](https://grafana.com/docs/alloy/latest/reference/cli/convert/) CLI (`--source-format=promtail`) to get a starting point. Be aware of the [converter limitations](https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/#limitations) — review the output manually before use.

   You can run the converter without installing Alloy locally:

   ```bash
   docker run \
     -v ./promtail.yaml:/etc/promtail/promtail.yaml \
     -v ./config.alloy:/etc/alloy/config.alloy \
     grafana/alloy:latest \
       convert --source-format=promtail --output=/etc/alloy/config.alloy /etc/promtail/promtail.yaml
   ```

   The input must be a fully rendered promtail config (no Ansible variables). Substitute real values before running the converter, then replace hardcoded host-specific values (hostnames, partition IDs, URLs, credentials) with Ansible variables (e.g. `{{ inventory_hostname }}`, `{{ metal_partition_id }}`) in the output.
   - **If the config is generally useful** (not environment-specific), consider contributing it as a new snippet to this role — see [Option B in Customizing the config](#customizing-the-config).
   - **If the config is specific to your environment**, use `alloy_config_raw` instead — see [Option A in Customizing the config](#customizing-the-config). Note that with `alloy_config_raw` you own the complete config, including the `loki.write "default"` block and its endpoint configuration; `alloy_loki_write_endpoints` is ignored.

5. **Update Prometheus inventory:** rename `prometheus_promtail_targets` → `prometheus_alloy_targets` (port `12345` instead of `9080`).

6. **Verify** that logs arrive in Loki with the correct labels. Check that existing dashboards and alerts still work as expected and adapt them for any label or metric name changes.

7. **Remove the promtail container** from the migrated hosts once verified:

   ```bash
   docker rm -f promtail
   rm -rf /etc/promtail
   ```

   The `promtail` role remains in this repo (deprecated) and does not need to be removed from your playbook — simply stop including it for migrated environments.
