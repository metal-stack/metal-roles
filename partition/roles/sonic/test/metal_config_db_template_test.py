import unittest

from test import read_template_file

from ansible.template import Templar


class MetalConfigDbTemplate(unittest.TestCase):
    def test_metal_config_db_template(self):
        t = read_template_file("metal.yaml.j2")

        templar = Templar(loader=None, variables=dict(
            inventory_hostname='r01mgmtleaf',
            sonic_mgmt_vrf="true",
            sonic_ntpservers=['1.2.3.4'],
            sonic_breakouts=dict(Ethernet0='4x25G'),
            sonic_ports=[dict(name='Ethernet0'),dict(name='Ethernet1'),dict(name='Ethernet2'),dict(name='Ethernet3'),dict(name='Ethernet50', speed=10000, mtu=9216, fec='rs'), dict(name='Ethernet51', speed=10000)],
            sonic_ports_default_mtu=9000,
            sonic_ports_default_fec=None,
            sonic_ports_default_speed=1000,
            sonic_loopback_address='10.0.0.1',
            sonic_bgp_ports=['Ethernet50', 'Ethernet51'],
            sonic_vlans=[dict(id=1, dhcp_servers=['10.255.255.254'], ip='10.255.255.1/24', untagged_ports=['Ethernet0', 'Ethernet1', 'Ethernet2', 'Ethernet3']),
                         dict(id=2, untagged_ports=['Ethernet4'])],
            sonic_vteps=[dict(vlan="Vlan2", vni="10002", comment="test-vtep")]
        ))

        res = templar.template(t)
        self.assertIn("""
DEVICE_METADATA:
  localhost:
    docker_routing_config_mode: split
    hostname: "r01mgmtleaf"

FEATURE:
  dhcp_relay:
    auto_restart: enabled
    state: enabled

NTP:
  global:
    src_intf: "eth0"

NTP_SERVER:
  1.2.3.4: {}

LOOPBACK_INTERFACE:
  Loopback0: {}
  Loopback0|10.0.0.1/32: {}

MGMT_VRF_CONFIG:
  vrf_global:
    mgmtVrfEnabled: true

BREAKOUT_CFG:
  Ethernet0:
    brkout_mode: "4x25G"

INTERFACE:
  Ethernet50:
    ipv6_use_link_local_only: enable
  Ethernet51:
    ipv6_use_link_local_only: enable

PORT:
  Ethernet0:
    admin_status: up
    speed: "1000"
    mtu: "9000"
    fec: "none"
  Ethernet1:
    admin_status: up
    speed: "1000"
    mtu: "9000"
    fec: "none"
  Ethernet2:
    admin_status: up
    speed: "1000"
    mtu: "9000"
    fec: "none"
  Ethernet3:
    admin_status: up
    speed: "1000"
    mtu: "9000"
    fec: "none"
  Ethernet50:
    admin_status: up
    speed: "10000"
    mtu: "9216"
    fec: "rs"
  Ethernet51:
    admin_status: up
    speed: "10000"
    mtu: "9000"
    fec: "none"

VLAN:
  Vlan1:
    dhcp_servers: ['10.255.255.254']
    vlanid: 1
  Vlan2:
    vlanid: 2

VLAN_INTERFACE:
  Vlan1: {}
  Vlan1|10.255.255.1/24: {}
  Vlan2: {}

VLAN_MEMBER:
  Vlan1|Ethernet0:
      tagging_mode: untagged
  Vlan1|Ethernet1:
      tagging_mode: untagged
  Vlan1|Ethernet2:
      tagging_mode: untagged
  Vlan1|Ethernet3:
      tagging_mode: untagged
  Vlan2|Ethernet4:
      tagging_mode: untagged

VXLAN_EVPN_NVO:
  nvo:
    source_vtep: vtep

VXLAN_TUNNEL:
  vtep:
    src_ip: "10.0.0.1"

VXLAN_TUNNEL_MAP:
  # test-vtep
  "vtep|map_10002_Vlan2":
    vlan: "Vlan2"
    vni: "10002"
""".strip(), res.strip())
