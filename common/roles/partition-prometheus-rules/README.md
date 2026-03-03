# partition-prometheus-rules

Contains default variables for partition prometheus alert manager rules. This way, they can be configured for both the control plane thanos rules and inside the prometheus in a partition.

## Variables

| Name                                         | Mandatory | Description                   |
| -------------------------------------------- | --------- | ----------------------------- |
| partition_prometheus_rules_blackbox_exporter |           | blackbox-exporter alert rules |
| partition_prometheus_rules_frr_exporter      |           | frr-exporter alert rules      |
| partition_prometheus_rules_haproxy           |           | haproxyalert rules            |
| partition_prometheus_rules_ipmi              |           | ipmi-exporter alert rules     |
| partition_prometheus_rules_leaf              |           | leaf switch alert rules       |
| partition_prometheus_rules_node_exporter     |           | node-exporter alert rules     |
| partition_prometheus_rules_pixiecore         |           | pixiecore alert rules         |
| partition_prometheus_rules_sonic_exporter    |           | sonic-exporter alert rules    |
