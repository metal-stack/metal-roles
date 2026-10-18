#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
import urllib.error
import urllib.request
import redis

INTERVAL = 60
CONFIG_DB = 4


def get_ifindex(interface):
    try:
        return int(open(f"/sys/class/net/{interface}/ifindex").read().strip())
    except (OSError, ValueError):
        return None


# The sflow packets contain the sampler address used to send the flow sample to the collector.
# This IP can be used to match the Interface to VRF mapping to a flow sample.
def get_sampler_address(db):
    for key in db.keys("SFLOW_COLLECTOR|*"):
        collector_ip = db.hget(key, "collector_ip")
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
    return db.hget(f"VRF|{vrf}", "vni")


def get_vrf_mappings(db, sampler_address):
    mappings = []

    for key in db.keys("INTERFACE|*"):
        try:
            _, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(key, "vrf_name")
        ifindex = get_ifindex(interface)
        if vrf and ifindex is not None:
            vni = get_vni(db, vrf)
            mappings.append({"interface": interface, "vrf": vrf, "vni": vni, "ifindex": ifindex, "sampler_address": sampler_address})

    for key in db.keys("VLAN_MEMBER|*"):
        try:
            _, vlan, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(f"VLAN_INTERFACE|{vlan}", "vrf_name")
        ifindex = get_ifindex(interface)
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
    db = redis.Redis(host="127.0.0.1", port=6379, db=CONFIG_DB, decode_responses=True)

    while True:
        sampler_address = get_sampler_address(db)
        # Refresh unchanged entries too: this renews their TTL and repopulates
        # Vector's memory table after a restart. Removed entries expire.
        publish_mappings(get_vrf_mappings(db, sampler_address), args.port)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
