# bgp-metrics

Writes BGP session metrics (`sonic_bgp_*`) to the node-exporter textfile collector. A systemd timer runs `vtysh -c "show bgp vrf all summary json"` and converts the output. Metric names and labels match the existing dashboards.

metal-core configures FRR directly, bypassing the SONiC management framework, so BGP state is not visible via gNMI or redis. vtysh is the only source and works on all SONiC switches.

## Variables

| Name                                       | Mandatory | Description                                |
| ------------------------------------------ | --------- | ------------------------------------------ |
| monitoring_bgp_metrics_textfile_directory  |           | node-exporter textfile collector directory |
| monitoring_bgp_metrics_interval            |           | Interval of the bgp-metrics timer          |
