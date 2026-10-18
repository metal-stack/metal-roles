#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
import urllib.error
import urllib.request

try:
    from swsscommon.swsscommon import SonicV2Connector
except ImportError:
    from swsssdk import SonicV2Connector

INTERVAL = 60


def get_ifindex(db, interface):
    # hsflowd exports the SONiC index, not the Linux index stored in "ifindex".
    value = db.get(db.STATE_DB, f"PORT_INDEX_TABLE|{interface}", "index", blocking=False)
    try:
        index = int(value)
    except (TypeError, ValueError):
        return None
    return index if index > 0 else None


# The sflow packets contain the sampler address used to send the flow sample to the collector.
# This IP can be used to match the Interface to VRF mapping to a flow sample.
def get_sampler_address(db):
    for key in db.keys(db.CONFIG_DB, "SFLOW_COLLECTOR|*") or []:
        collector_ip = db.get(db.CONFIG_DB, key, "collector_ip", blocking=False)
        if not collector_ip:
            continue
        try:
            tokens = subprocess.run(
                ["ip", "route", "get", collector_ip],
                capture_output=True, text=True, timeout=5,
            ).stdout.split()
            if "src" in tokens:
                return tokens[tokens.index("src") + 1]
        except Exception:
            pass
    return None


def get_vni(db, vrf):
    return db.get(db.CONFIG_DB, f"VRF|{vrf}", "vni", blocking=False)


def get_vrf_mappings(db, sampler_address):
    mappings = []

    for key in db.keys(db.CONFIG_DB, "INTERFACE|*") or []:
        try:
            _, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.get(db.CONFIG_DB, key, "vrf_name", blocking=False)
        ifindex = get_ifindex(db, interface)
        if vrf and ifindex is not None:
            vni = get_vni(db, vrf)
            mappings.append({"interface": interface, "vrf": vrf, "vni": vni, "ifindex": ifindex, "sampler_address": sampler_address})

    for key in db.keys(db.CONFIG_DB, "VLAN_MEMBER|*") or []:
        try:
            _, vlan, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.get(db.CONFIG_DB, f"VLAN_INTERFACE|{vlan}", "vrf_name", blocking=False)
        ifindex = get_ifindex(db, interface)
        if vrf and ifindex is not None:
            vni = get_vni(db, vrf)
            mappings.append({"interface": interface, "vlan": vlan, "vrf": vrf, "vni": vni, "ifindex": ifindex, "sampler_address": sampler_address})

    return mappings


def publish_mappings(mappings, port):
    # Match the composite key used by Vector's enrich_vrf transform.
    # Duplicates may appear on hybrid ports; keep the last mapping as before.
    records = {}
    for entry in mappings:
        if not entry.get("sampler_address") or entry.get("ifindex") is None:
            continue
        key = f"{entry['sampler_address']}|{entry['ifindex']}"
        records[key] = {
            field: str(entry.get(field) or "")
            for field in ("interface", "vrf", "vni")
        }
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/ifindex",
        data=json.dumps({"mappings": records}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        # Never send local mappings through a proxy inherited from the host.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(request, timeout=5):
            pass
    except (OSError, urllib.error.URLError) as exc:
        # Vector may still be starting or restarting. Retry at the next refresh.
        print(f"vrf-port-export: failed to publish mappings: {exc}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Publish interface mappings to Vector")
    parser.add_argument("--port", type=int, default=9001)
    args = parser.parse_args()
    db = SonicV2Connector(host="127.0.0.1", decode_responses=True)
    db.connect(db.CONFIG_DB)
    db.connect(db.STATE_DB)

    while True:
        sampler_address = get_sampler_address(db)
        # Refresh unchanged entries too: this renews their TTL and repopulates
        # Vector's memory table after a restart. Removed entries expire.
        publish_mappings(get_vrf_mappings(db, sampler_address), args.port)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
