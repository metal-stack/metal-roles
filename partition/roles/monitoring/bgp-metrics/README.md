# bgp-metrics

Writes BGP session metrics (`sonic_bgp_*`) and FRR route counts (`sonic_routes_rib`, `sonic_routes_fib`) to the node-exporter textfile collector. A systemd timer runs `vtysh -c "show bgp vrf all summary json"` plus `show ip/ipv6 route vrf <name> summary json` per active VRF and converts the output. Metric names and labels match the existing dashboards.

Route counts are queried per VRF because `show ip route vrf all summary json` on unpatched FRR 8.x prints one bare JSON object per VRF without VRF names, which cannot be parsed.

metal-core configures FRR directly, bypassing the SONiC management framework, so BGP state is not visible via gNMI or redis. vtysh is the only source and works on all SONiC switches.

## Variables

| Name                                       | Mandatory | Description                                |
| ------------------------------------------ | --------- | ------------------------------------------ |
| monitoring_bgp_metrics_textfile_directory  |           | node-exporter textfile collector directory |
| monitoring_bgp_metrics_interval            |           | Interval of the bgp-metrics timer          |
