import unittest

import yaml
import os
from textwrap import dedent

from ansible.template import Templar

from test import read_template_file


def read_defaults():
    with open(os.path.join(os.path.dirname(__file__), "..", "defaults", "main.yaml"), "r") as stream:
        return yaml.safe_load(stream)


class MgmtServerFrrConf(unittest.TestCase):
    maxDiff = None

    def test_frr_conf_template(self):
        t = read_template_file("frr.conf.j2")

        templar = Templar(loader=None, variables=read_defaults() | dict(
            ansible_hostname="mgmt01",
            mgmt_server_asn=4200000000,
            mgmt_server_router_id="10.1.0.1",
            mgmt_server_spine_facing_interface="lan0",
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        frr defaults datacenter
        hostname mgmt01
        !
        service integrated-vtysh-config
        !
        log syslog debugging
        debug bgp updates
        debug bgp nht
        debug bgp update-groups
        debug bgp zebra
        !
        interface lan0
         ipv6 nd ra-interval 6
         no ipv6 nd suppress-ra
        !
        router bgp 4200000000
         bgp router-id 10.1.0.1
         bgp bestpath as-path multipath-relax
         bgp network import-check
         neighbor FABRIC peer-group
         neighbor FABRIC remote-as external
         neighbor FABRIC timers 1 3
         neighbor lan0 interface peer-group FABRIC
          !
         address-family ipv4 unicast
          redistribute connected route-map LOCAL_INTERFACES
           exit-address-family
        !
        route-map LOCAL_INTERFACES permit 10
          match interface lo
        !
        line vty
        !
        """), result)

    def test_frr_conf_template_with_firewall_static_routes_and_default_route(self):
        t = read_template_file("frr.conf.j2")

        templar = Templar(loader=None, variables=read_defaults() | dict(
            ansible_hostname="mgmt01",
            mgmt_server_asn=4200000000,
            mgmt_server_router_id="10.1.0.1",
            mgmt_server_spine_facing_interface="lan0",
            mgmt_server_firewall_ip="10.1.0.2",
            mgmt_server_provide_default_route=True,
            mgmt_server_frr_static_routes=[
                "10.100.0.0/22 10.1.0.254",
                "192.168.0.0/16 10.1.0.253",
            ],
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        frr defaults datacenter
        hostname mgmt01
        !
        service integrated-vtysh-config
        !
        log syslog debugging
        debug bgp updates
        debug bgp nht
        debug bgp update-groups
        debug bgp zebra
        !
        ip route 10.100.0.0/22 10.1.0.254
        ip route 192.168.0.0/16 10.1.0.253
        !
        interface lan0
         ipv6 nd ra-interval 6
         no ipv6 nd suppress-ra
        !
        router bgp 4200000000
         bgp router-id 10.1.0.1
         bgp bestpath as-path multipath-relax
         bgp network import-check
         neighbor FABRIC peer-group
         neighbor FABRIC remote-as external
         neighbor FABRIC timers 1 3
         neighbor lan0 interface peer-group FABRIC
          neighbor 10.1.0.2 peer-group FABRIC
         neighbor 10.1.0.2 disable-connected-check
          !
         address-family ipv4 unicast
          redistribute connected route-map LOCAL_INTERFACES
            network 0.0.0.0/0
           exit-address-family
        !
        route-map LOCAL_INTERFACES permit 10
          match interface lo
        !
        line vty
        !
        """), result)


class MgmtServerSSHConfig(unittest.TestCase):
    maxDiff = None

    def test_ssh_config_template(self):
        t = read_template_file("ssh_config.j2")

        # leaf02 comes before leaf01 to prove hosts are rendered in sorted
        # order, mgmt01 has no ansible_user and must be skipped entirely
        templar = Templar(loader=None, variables=read_defaults() | dict(
            mgmt_server_metal_ssh_options=["StrictHostKeyChecking no"],
            mgmt_server_metal_ssh_groups=["leaf02", "mgmt01", "leaf01"],
            hostvars=dict(
                leaf01=dict(ansible_host="10.1.0.10", ansible_user="admin", host_alias="exit01"),
                leaf02=dict(ansible_host="10.1.0.11", ansible_user="admin"),
                mgmt01=dict(ansible_host="10.1.0.1"),
            ),
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        StrictHostKeyChecking no
        Host leaf01 exit01
                User admin
        Host leaf02{trailing_space}
                User admin
        """).format(trailing_space=" "), result)


class MgmtServerResolvedConf(unittest.TestCase):
    maxDiff = None

    def test_resolved_conf_template_with_defaults(self):
        t = read_template_file("resolved.conf.j2")

        templar = Templar(loader=None, variables=read_defaults())

        result = templar.template(t)

        self.assertEqual(dedent("""\
        [Resolve]
        DNS=193.110.81.0#dns0.eu
        DNS=2a0f:fc80::#dns0.eu
        DNS=185.253.5.0#dns0.eu
        DNS=2a0f:fc81::#dns0.eu

        DNSOverTLS=yes
        """), result)

    def test_resolved_conf_template_without_dns_over_tls(self):
        t = read_template_file("resolved.conf.j2")

        templar = Templar(loader=None, variables=read_defaults() | dict(
            mgmt_server_nameservers=["10.1.0.53"],
            mgmt_server_dns_over_tls=False,
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        [Resolve]
        DNS=10.1.0.53

        """), result)


class MgmtServerDockerDaemonJson(unittest.TestCase):
    maxDiff = None

    def test_daemon_json_template(self):
        t = read_template_file("daemon.json.j2")

        templar = Templar(loader=None, variables=read_defaults())

        result = templar.template(t, convert_data=False)

        self.assertEqual(dedent("""\
        {
            "registry-mirrors": ["https://mirror.gcr.io"]
        }"""), result)
