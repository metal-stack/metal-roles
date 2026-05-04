# sFlow Monitoring: Design and Architecture

This document describes how the network flow monitoring pipeline in this branch works.

## Problem Statement

Metal-stack partitions run SONiC switches to carry tenant traffic. Before this work there was limited visibility into which protocols, hosts, or VRFs were generating that traffic, which made it hard to diagnose anomalies or attribute usage. The aim was to add flow-level visibility without deploying a dedicated analytics platform.

## High-Level Architecture

```text
SONiC Switches (partition)
  │
  │  sFlow 
  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Kubernetes Pod: goflow2 (control-plane, monitoring namespace)           │
│                                                                         │
│  ┌──────────┐  stdout JSON    ┌────────────────────────────────────┐    │
│  │ goflow2  │ ──────────────► │ Vector sidecar                     │    │
│  │ collector│                 │  1. parse goflow2 JSON             │    │
│  └──────────┘                 │  2. enrich: protocol classification│    │
│                               │  3. enrich: VRF / interface name   │    │
│  ┌───────────────┐            │  4. sample + enrich: geo-IP        │    │
│  │ vrf-csv-      │            │  5. sink → Loki (two streams)      │    │
│  │ builder       │──────────► │                                    │    │
│  │ (sidecar)     │ ifindex.csv└────────────────────────────────────┘    │
│  └───────────────┘                                                      │
└─────────────────────────────────────────────────────────────────────────┘
         ▲
         │  HTTP query (Loki API)
         │
┌────────┴───────────┐
│       Loki         │◄─── promtail (switch) ◄─── vrf-port-export.py (switch)
│                    │                              reads SONiC config-db
└────────────────────┘
         │
         ▼
┌────────────────────┐
│   Grafana          │  sFlow analytics dashboard
│   (Prometheus)     │  Network Weathermap (LLDP)
└────────────────────┘
```

---

## Flow Collection: goflow2

[goflow2](https://github.com/netsampler/goflow2) is a stateless flow collector that speaks sFlow, NetFlow, and IPFIX. It was picked over pmacct, nfdump, and ntopng for a few reasons:

- It is one Go binary that translates sFlow UDP packets to structured JSON. No database, no UI, no persistent state.
- It supports JSON, Protobuf, and Avro output. Json is chosen because it drops straight into Vector's `parse_json` transform.
- The `-addr` flag exposes Prometheus metrics, so collector health (packets received, unknown samples, decode errors) comes for free.

---

## Flow Enrichment: Vector as a Sidecar

Enrichment runs in a Vector sidecar container in the same pod rather than inside goflow2, which would have meant forking it or writing a plugin. goflow2 owns the network protocol and Vector owns the data transformation pipeline.

### Log-file coupling between goflow2 and Vector

There are multiple options to handle the flow samples between receiving the sample in goflow2 and enriching them in vector. 

In this case goflow2 and vector are containers in the same pod. Inside the goflow2 container, goflow2 writes JSON to a named pipe at `/tmp/flows.fifo`. A netcat `nc` process reads from the pipe and forwards each line to `127.0.0.1:{{ sflow_collector_internal_port }}`, where Vector's TCP `socket` source is listening. If vector slows down and the buffer fills up, flow samples will be lost. This is acceptable as flow sampling is sampling 1 in n packets and thus lossy to begin with.

Other options that were considered are writing flow logs to disk via stdout and reading them via vector. This is straight forward and headroom to buffer logs in case the enrichment pipeline breaks is affordable. Additionally k8s natively handles log rotation. The significant drawback here is that logs are written to disk twice. This is also the slowest possible implementation. A similar approach can be implemented in memory to gain back performance, however this requires additional effort, as there is no automatic log rotation and the pod will eventually run out of memory.

### Enrichment pipeline stages

Vector processes each flow through a chain of `remap` transforms.

`parse_goflow2` parses the JSON payload, normalises integer fields (ports, interface index), and sets defaults for fields that later stages will fill in (`vrf = "default"`, `app_proto = "UNCLASSIFIED"`).

`enrich_proto` looks up the destination port in the `well_known_ports` enrichment table (currently a static table). The destination port is checked first because sFlow typically samples ingress traffic on uplinks, so the destination port most likely identifies the service that tenant clusters are offering. If neither port matches a known protocol, the port number itself is stored as the `app_proto` label. That keeps unknown ports queryable instead of collapsing them all into one "unknown" bucket.

`enrich_vrf` looks up the `(sampler_address, ifindex)` pair in the `ifindex_vrf` enrichment table (see [VRF enrichment pipeline](#vrf-enrichment-pipeline)). On a match the flow record gains `vrf`, `vni`, and `interface` fields. On no match `vrf` stays `"default"`, which is the right value for traffic on SONiC interfaces not bound to a specific VRF.

`geo_sample` and `enrich_geo` push a configurable fraction of flows (`vector_goflow2_geo_sample_rate`) through a geo-IP lookup. Sampling happens here rather than globally because geo-IP adds significant log volume and most internal traffic (RFC 1918 addresses) would produce no useful result. Private, loopback, and link-local prefixes are dropped before the lookup.

### Two Loki output streams

Vector writes to two separate Loki streams:

| Stream | Input | Loki labels | Purpose |
| ------ | ----- | ----------- | ------- |
| `loki_goflow2` | `enrich_vrf` | `proto_name`, `app_proto`, `vrf`, `sampler_address` | All flows; supports VRF/protocol dashboards |
| `loki_geo` | `enrich_geo` | (none beyond `app`) | Sampled flows with geo coordinates; supports map panels |

Splitting the streams has two upsides: the geo stream is much smaller (sampled) and can use different retention, and queries against the main stream are not slowed by the extra geo coordinate fields.

The labels on the main stream were picked to keep Loki's index small. High-cardinality values like source IP, destination IP, and port number stay as log line fields. Only low-cardinality dimensions (`vrf`, `proto_name`, `app_proto`, `sampler_address`) are promoted to labels.

---

## VRF Enrichment Pipeline

Goflow2 receives sFlow packets containing an interface index (`ifindex`) and the IP of the sending switch (`sampler_address`). The best way to stitch VRF information to a flow sample depends on where the sample was taken, and if that sampled packet was VXLAN encapsulated or not. For this reason the branch implements multiple approaches to match a flow to a VRF. If the sample was taken on a machine facing port the correlation is easy. Metal-stack binds every machine facing port to a VRF. This infomration can be directly read from redis. If traffic is only sampled on fabric uplinks and not on downlinks the ifindex will not resolve to a tenant VRF. In this case tenant traffic can safely be assumed to be VXLAN encapsulated. sFLow also transmits the VNI contained in the VXLAN header. The VNI can be used to attribute traffic to the tenant VRF. If no match is found, it is assumed that the traffic belongs to the default VRF. 

### `vrf-port-export.py` (on the switch)

A systemd service on every SONiC switch. Every 60 seconds it:

1. Queries Redis `config-db` for `INTERFACE|*` keys (routed ports) and `VLAN_MEMBER|*` keys (access/trunk ports), collecting each interface's VRF binding.
2. Reads `/sys/class/net/<iface>/ifindex` to get the kernel interface index. This is the same value that appears in sFlow packets.
3. Works out the switch's own source IP using a routing routing lookup toward the sFlow collector with `ip route get`. That IP is the `sampler_address` goflow2 will report.
4. Writes all mappings as JSON lines to `/var/log/vrf-interface-mapping.log`, using an atomic rename write to safe space while allowing promtail to see changes to the file.

promtail on the switch picks up that log file and forwards it to Loki in the control plane.

### `vrf-csv-builder.py` (sidecar in the collector pod)

This sidecar queries Loki every 60 seconds for VRF mapping entries from the last 5 minutes. It deduplicates by `(sampler_address, ifindex)`, keeps the most recent entry per pair, and writes a CSV to a shared `emptyDir` volume that Vector mounts as an enrichment table.

---

## GeoIP Enrichment

The init container downloads the [DB-IP City Lite](https://db-ip.com/db/lite/city) database when the pod starts. DB-IP was picked over MaxMind GeoLite2 because it does not need an account or a license key. The init container tries the current month's file first and falls back to the previous month, since the database is published monthly and the current month's file may not yet exist on the first.

The geo stream is sampled (configurable via `vector_goflow2_geo_sample_rate`) instead of running every flow through geo-IP. The geo dashboard (map view) does not need per-flow precision. Sampled data still gives a representative picture of where traffic is coming from.

