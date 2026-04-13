#!/usr/bin/env python3

from collections.abc import Sequence
import argparse
import ipaddress
import logging
import sys
import subprocess
import signal
import os


DEFAULT_DHCPD_LEASE_FILE = '/var/lib/dhcp/dhcpd.leases'
DEFAULT_IPMI_EXPORTER_FILE_SD = '/etc/prometheus/file_sd/ipmi.yaml'

IPMI_EXPORTER_FILE_SD_PREAMBLE = """---
- labels:
    job: ipmi
  targets:
"""


class IpmiTargetWriter:
    def __init__(self,
                 allowed_cidrs: Sequence[str],
                 ipmi_exporter_file: str,
                 dhcpd_lease_file: str):
        self.allowed_cidrs = allowed_cidrs
        self.ipmi_exporter_file = ipmi_exporter_file
        self.dhcpd_lease_file = dhcpd_lease_file

    def run(self):
        ips = self.ips_from_dhcpd_lease_file()
        ips = self.filter_ips(ips)

        with open(self.ipmi_exporter_file, "w") as targets:
            # we do not use yaml dump because this would require another dependency
            targets.write(IPMI_EXPORTER_FILE_SD_PREAMBLE)

            for ip in ips:
                targets.write("    - " + str(ip) + "\n")

        logging.info("successfully written ipmi-exporter targets file at %s" %
                     self.ipmi_exporter_file)

        # we do not need to trigger a config reload of prometheus,
        # it watches the file_sd directory and reloads automatically

    def ips_from_dhcpd_lease_file(self):
        ips = []

        logging.info("reading dhcpd lease file at %s" % self.dhcpd_lease_file)

        with open(self.dhcpd_lease_file, 'r') as lease_file:
            for line in lease_file.readlines():
                line = line.strip()

                if not line.startswith("lease "):
                    continue
                if not line.endswith(" {"):
                    continue

                line = line.removeprefix("lease ").removesuffix(" {")

                try:
                    ip = ipaddress.ip_address(line)
                except ValueError as e:
                    logging.warning("unable to parse ip address: %s" % e)
                    continue

                if ip not in ips:
                    ips.append(ip)

        return ips

    def filter_ips(self, ips):
        allowed_networks = []
        filtered = []

        for network in self.allowed_cidrs:
            try:
                allowed_networks.append(ipaddress.ip_network(network))
            except ValueError as e:
                logging.warning("unable to parse ip network: %s" % e)
                continue

        for ip in ips:
            if allowed_networks:
                skip = True

                for nw in allowed_networks:
                    if ip in nw:
                        skip = False
                        break

                if skip:
                    logging.info("filtered out ip address: %s" % str(ip))
                    continue

            logging.info("including ip address in target file: %s" % str(ip))
            filtered.append(ip)

        return filtered


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dhcpd-lease-file", help="the path to the dhcpd lease file", default=DEFAULT_DHCPD_LEASE_FILE)
    parser.add_argument("--prometheus-ipmi-file-sd",
                        help="the path to prometheus ipmi file sd file", default=DEFAULT_IPMI_EXPORTER_FILE_SD)
    parser.add_argument(
        "allowed_cidrs", help="filters ips for the given allowed cidrs", nargs='*')

    args = parser.parse_args()

    IpmiTargetWriter(allowed_cidrs=args.allowed_cidrs, dhcpd_lease_file=args.dhcpd_lease_file,
                     ipmi_exporter_file=args.prometheus_ipmi_file_sd).run()
