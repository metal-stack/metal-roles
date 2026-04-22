#!/usr/bin/env python3
"""
Maps Ethernet and VLAN Interfaces to VRFs using redis. It is assumed here
that either the Ethernet Port or the SVI is assigned to a VRF not both.
"""

import json
import os
import time
import redis
from datetime import datetime, timezone

LOG_FILE = "/var/log/vrf-interface-mapping.log"
LOG_FILE_TMP = LOG_FILE + ".tmp"
INTERVAL = 60
CONFIG_DB = 4


def get_vrf_mappings(db: redis.Redis) -> list[dict]:
    mappings = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for key in db.keys("INTERFACE|*"):
        try:
            _, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(key, "vrf_name")
        if vrf:
            mappings.append({"ts": ts, "interface": interface, "vrf": vrf})

    for key in db.keys("VLAN_MEMBER|*"):
        try:
            _, vlan, interface = key.split("|")
        except ValueError:
            continue
        vrf = db.hget(f"VLAN_INTERFACE|{vlan}", "vrf_name")
        if vrf:
            mappings.append({"ts": ts, "interface": interface, "vlan": vlan, "vrf": vrf})

    return mappings


def main():
    db = redis.Redis(host="127.0.0.1", port=6379, db=CONFIG_DB, decode_responses=True)

    while True:
        with open(LOG_FILE_TMP, "w") as log:
            for entry in get_vrf_mappings(db):
                log.write(json.dumps(entry) + "\n")
        os.replace(LOG_FILE_TMP, LOG_FILE)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
