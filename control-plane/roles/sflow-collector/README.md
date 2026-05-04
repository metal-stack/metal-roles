# sflow-collector

Deploys [goflow2](https://github.com/netsampler/goflow2) as an sFlow UDP collector alongside a Vector sidecar for flow enrichment. Receives sFlow packets from SONiC switches. 

You can look up all the default values of this role [here](defaults/main.yaml).

## Variables

| Name                                    | Mandatory | Description                                                   |
| --------------------------------------- | --------- | ------------------------------------------------------------- |
| `sflow_collector_namespace`             |           | Kubernetes namespace to deploy into                           |
| `sflow_collector_image`                 | yes       | goflow2 container image                                       |
| `sflow_collector_port`                  |           | UDP port to receive sFlow packets on (default: 6343)          |
| `sflow_collector_metrics_port`          |           | Port exposing Prometheus metrics (default: 9099)              |
| `sflow_collector_geoip_download_image`  |           | Image used to download the MaxMind GeoIP database             |
| `sflow_collector_vrf_csv_builder_image` |           | Image used to build the VRF-to-interface CSV                  |
| `sflow_collector_vector_resources`      |           | Resource requests and limits for the Vector sidecar container |
