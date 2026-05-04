# vector-goflow2

Deploys the Vector ConfigMaps for the sflow-collector sidecar. Provides enrichment data for VRF name lookup, well-known port classification, interface index mapping, and geo-IP sampling of flow records.

You can look up all the default values of this role [here](defaults/main.yaml).

## Variables

| Name                              | Mandatory | Description                                                              |
| --------------------------------- | --------- | ------------------------------------------------------------------------ |
| `sflow_collector_namespace`       |           | Namespace where ConfigMaps are created (shared with the sflow-collector) |
| `vector_goflow2_vector_image`     | yes       | Vector container image                                                   |
| `vector_goflow2_geo_sample_rate`  |           | Fraction of flows sampled for geo-IP enrichment (1 = every flow)         |
