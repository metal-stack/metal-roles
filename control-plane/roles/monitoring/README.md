# monitoring

This role is designed to set up monitoring for a Linux-based system using Ansible. 
The role includes tasks to install and configure the following monitoring tools:
-    Prometheus
-     Grafana
-    Node Exporter
-    Alertmanager
-    Thanos

## Variables

This role uses variables from [control-plane-defaults](/control-plane). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).
The following variables can be set to configure the role:
-    prometheus_version: The version of Prometheus to install (default: 2.26.0)
-    grafana_version: The version of Grafana to install (default: 7.1.5)
-    node_exporter_version: The version of Node Exporter to install (default: 0.18.1)

### General

| Name                               | Mandatory | Description                                                                                                                        |
|------------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------|
| metal_monitoring_namespace          |           | Naming of the newly created namespace           
|      prometheus_version             |  
|      grafana_version                |  
|      node_exporter_version          |     

