#!/usr/bin/env python3
import csv
import os
import subprocess
import time
import redis

CSV_FILE = "/var/lib/sflow-collector/ifindex.csv"
CSV_FILE_TMP = CSV_FILE + ".tmp"
CSV_FIELDS = ["sampler_address", "ifindex", "interface", "vrf", "vni"]
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


def write_csv(mappings):
    # Vector's ifindex_vrf enrichment table is keyed on (sampler_address, ifindex);
    # Duplicates may appear on hybrid ports. Not expected in production.
    deduped = {}
    for entry in mappings:
        key = (entry.get("sampler_address") or "", entry.get("ifindex"))
        deduped[key] = entry
    try:
        with open(CSV_FILE_TMP, "w", newline="") as csv_fp:
            writer = csv.DictWriter(csv_fp, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            for entry in deduped.values():
                writer.writerow({k: ("" if entry.get(k) is None else entry.get(k)) for k in CSV_FIELDS})
        os.replace(CSV_FILE_TMP, CSV_FILE)
    except OSError as exc:
        print(f"vrf-port-export: skipping CSV write: {exc}", flush=True)


def main():
    db = redis.Redis(host="127.0.0.1", port=6379, db=CONFIG_DB, decode_responses=True)

    while True:
        sampler_address = get_sampler_address(db)
        write_csv(get_vrf_mappings(db, sampler_address))
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
