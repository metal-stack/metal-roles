# lldp-weathermap

Generates a Grafana canvas dashboard that visualizes network topology and live link utilization. Topology is derived from LLDP data collected from switches at deploy time. Nodes are organized into configurable tiers (e.g. spine, exit, leaf) and links are color-coded against configurable bandwidth thresholds.

You can look up all the default values of this role [here](defaults/main.yaml).

## Variables

| Name                               | Mandatory | Description                                                                                       |
| ---------------------------------- | --------- | ------------------------------------------------------------------------------------------------- |
| `lldp_weathermap_namespace`        |           | Kubernetes namespace for the Grafana dashboard ConfigMap                                          |
| `lldp_weathermap_dashboard_name`   |           | Display name of the Grafana dashboard                                                             |
| `lldp_weathermap_tiers`            |           | List of tier definitions; each entry has `id`, `top_fraction`, `background_color`, `border_color` |
| `lldp_weathermap_fallback_tier`    |           | Tier assigned to nodes not matching any known tier id                                             |
| `lldp_weathermap_panel_grid_rows`  |           | Grid row height of the canvas panel                                                               |
| `lldp_weathermap_thresholds`       |           | Link utilization thresholds mapping bps values to display colors                                  |
| `lldp_weathermap_hosts_group`      | yes       | Ansible inventory group to collect LLDP data from                                                 |
| `lldp_weathermap_node_filter`      |           | List of tier IDs to include in the weathermap; nodes in other tiers are hidden                    |
| `lldp_weathermap_static_links`     |           | Static link definitions that can't be autodiscovered using LLDP                                   |
