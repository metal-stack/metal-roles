import unittest

from test import read_template_file

from ansible.template import Templar


class FrrTemplate(unittest.TestCase):
    def test_frr_template(self):
        t = read_template_file("frr.conf.j2")

        templar = Templar(loader=None, variables=dict(
            ansible_hostname='r01mgmtleaf',
            sonic_asn='420000000',
            sonic_static_routes=[],
            sonic_loopback_address='10.0.0.1',
            sonic_bgp_ports=['Ethernet50', 'Ethernet51'],
            sonic_frr_syslog_level='debug'
        ))

        res = templar.template(t)
        self.assertIn("""
frr defaults datacenter
hostname r01mgmtleaf
username cumulus nopassword
!
service integrated-vtysh-config
!
log syslog debug
!
interface Ethernet50
 ipv6 nd ra-interval 6
 no ipv6 nd suppress-ra
!
interface Ethernet51
 ipv6 nd ra-interval 6
 no ipv6 nd suppress-ra
!
router bgp 420000000
 bgp router-id 10.0.0.1
 bgp bestpath as-path multipath-relax
 neighbor FABRIC peer-group
 neighbor FABRIC remote-as external
 neighbor FABRIC timers 1 3
 neighbor Ethernet50 interface peer-group FABRIC
 neighbor Ethernet51 interface peer-group FABRIC
 !
 address-family ipv4 unicast
  redistribute connected
 exit-address-family
!
line vty
!
""".strip(), res.strip())
