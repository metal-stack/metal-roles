#!/usr/bin/python3
import json
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("asn", help="BGP autonomous system number")
parser.add_argument("file", help="file containing BGP neighbors to remove")
args = parser.parse_args()

peer_group_cmd = ["vtysh", "-c", "show bgp peer-group json"]

try:
    peer_group_result = subprocess.run(peer_group_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
except subprocess.CalledProcessError as e:
    sys.stderr.write(e.stderr.decode())
    sys.exit(1)

try:
    peer_groups = json.loads(peer_group_result.stdout.decode())
except json.JSONDecodeError as e:
    sys.stderr.write(f"Error decoding JSON output: {e}\n")
    sys.exit(1)

if "FIREWALL" not in peer_groups and "members" not in peer_groups["FIREWALL"]:
    print("Nothing to do, because peer group FIREWALL is empty.")
    sys.exit(0)

peers = peer_groups["FIREWALL"]["members"]
remove_cmd = ["vtysh", "-c", "configure terminal", "-c", f"router bgp {args.asn}"]
removed_neighbors = []
with open(args.file) as f:
    for line in f:
        neighbor = line.strip()
        if neighbor in peers:
            remove_cmd += ["-c", f"no neighbor {neighbor}"]
            removed_neighbors.append(neighbor)

if len(removed_neighbors) == 0:
    print("Nothing to do.")
    sys.exit(0)

remove_result = subprocess.run(remove_cmd, stderr=subprocess.PIPE)

# Check return code and print error message if necessary
if remove_result.returncode != 0:
    sys.stderr.write(remove_result.stderr.decode())
    sys.exit(1)

print(f"Removed neighbors: {' '.join(removed_neighbors)}")
