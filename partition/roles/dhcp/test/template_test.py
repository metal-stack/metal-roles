import os
import unittest
from textwrap import dedent

from ansible.template import Templar


def read_template_file(name):
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", name), 'r') as f:
        return f.read()


class DHCPD(unittest.TestCase):
    def test_dhcpd_config_template(self):
        t = read_template_file("dhcpd.conf.j2")

        templar = Templar(loader=None, variables=dict(
            dhcp_subnets=[
                dict(
                    comment="testing",
                    network="1.2.3.4",
                    netmask="24",
                    range=dict(begin=1, end=2),
                    options=["routers 2.2.2.2", "domain-name-servers 1.1.1.1, 8.8.8.8"],
                    deny_list=["unknown-clients"],
                ),
            ],
            dhcp_default_lease_time=600,
            dhcp_max_lease_time=600,
            dhcp_global_options=[],
            dhcp_global_deny_list=[],
            groups=dict(mgmt_servers=["mgmt01", "mgmt02"]),
            hostvars=dict(mgmt01=dict(switch_mgmt_ip="3.3.3.3"), mgmt02=dict(switch_mgmt_ip="4.4.4.4")),
            dhcp_use_host_decl_names=False,
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        # indicate that the DHCP server should send DHCPNAK messages to misconfigured client
        authoritative;
        
        default-lease-time 600;
        max-lease-time 600;
        
        log-facility local7;
        
        # testing
        subnet 1.2.3.4 netmask 24 {
          range 1 2;
          option routers 2.2.2.2;
          option domain-name-servers 1.1.1.1, 8.8.8.8;
          deny unknown-clients;
        }
        """), result)

    def test_dhcpd_hosts_config_template(self):
        t = read_template_file("dhcpd.hosts.j2")

        templar = Templar(loader=None, variables=dict(
            dhcp_static_hosts=[
                dict(
                    name="test1",
                    mac="aa:bb:cc:dd:ee:ef",
                    ip="10.1.2.1",
                    options=['test1']
                ),
                dict(
                    name="test2",
                    mac="aa:bb:cc:dd:ee:ff",
                    ip="10.1.2.2",
                    options=['test2']
                )
            ],
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        host test1 {
          hardware ethernet aa:bb:cc:dd:ee:ef;
          fixed-address 10.1.2.1;
          option test1;
        }
        
        host test2 {
          hardware ethernet aa:bb:cc:dd:ee:ff;
          fixed-address 10.1.2.2;
          option test2;
        }
        
        """), result)
