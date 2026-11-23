#!/usr/bin/env python3
import argparse
import ipaddress
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


def get_sampler_address():
    # Read hsflowd's selected agent address, which identifies the sampler in
    # sFlow datagrams even when the collector route uses a different source IP.
    try:
        result = subprocess.run(
            ["docker", "exec", "sflow", "cat", "/etc/hsflowd.auto"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        settings = {}
        for line in result.stdout.splitlines():
            key, separator, value = line.partition("=")
            if separator:
                settings[key.strip()] = value.strip()
        # hsflowd rewrites this file in place; reject an incomplete snapshot.
        if not settings.get("rev_start") or settings["rev_start"] != settings.get("rev_end"):
            raise ValueError("incomplete hsflowd configuration")
        address = ipaddress.ip_address(settings.get("agentIP"))
        if address.is_unspecified:
            raise ValueError("hsflowd has not selected an agent address")
        return str(address)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"vrf-port-export: sampler address unavailable: {exc}", flush=True)
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
        sampler_address = get_sampler_address()
        # Refresh unchanged entries too: this renews their TTL and repopulates
        # Vector's memory table after a restart. Removed entries expire.
        publish_mappings(get_vrf_mappings(db, sampler_address), args.port)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
