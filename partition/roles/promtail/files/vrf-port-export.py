#!/usr/bin/env python3
import json
import os
import subprocess
import time
import redis
from datetime import datetime, timezone

LOG_FILE = "/var/log/vrf-interface-mapping.log"
LOG_FILE_TMP = LOG_FILE + ".tmp"
INTERVAL = 60
CONFIG_DB = 4


def get_ifindex(interface):
    try:
        return int(open(f"/sys/class/net/{interface}/ifindex").read().strip())
    except (OSError, ValueError):
        return None


# The sflow packets contain the sampler address used to send the flow samp€e to the collector.
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


def get_vrf_mappings(db, sampler_address):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mappings = []

    for key in db.keys("INTERFACE|*"):
        try:
            _, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(key, "vrf_name")
        ifindex = get_ifindex(interface)
        if vrf and ifindex is not None:
            mappings.append({"ts": ts, "interface": interface, "vrf": vrf, "ifindex": ifindex, "sampler_address": sampler_address})

    for key in db.keys("VLAN_MEMBER|*"):
        try:
            _, vlan, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(f"VLAN_INTERFACE|{vlan}", "vrf_name")
        ifindex = get_ifindex(interface)
        if vrf and ifindex is not None:
            mappings.append({"ts": ts, "interface": interface, "vlan": vlan, "vrf": vrf, "ifindex": ifindex, "sampler_address": sampler_address})

    return mappings


def main():
    db = redis.Redis(host="127.0.0.1", port=6379, db=CONFIG_DB, decode_responses=True)

    while True:
        sampler_address = get_sampler_address(db)
        with open(LOG_FILE_TMP, "w") as log:
            for entry in get_vrf_mappings(db, sampler_address):
                log.write(json.dumps(entry) + "\n")
        os.replace(LOG_FILE_TMP, LOG_FILE)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
