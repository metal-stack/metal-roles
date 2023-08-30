import unittest

from test import read_template_file

from ansible.template import Templar


class SystemdNetworkdTemplates(unittest.TestCase):
    def test_template_inet_router(self):
        self.maxDiff = None

        vars = dict(
            systemd_networkd_mtu=9000,
            systemd_networkd_nics=[],
            systemd_networkd_vrfs=[],
            systemd_networkd_vxlans=[],
            systemd_networkd_vlans=[],
        )

        vars.update(item=dict(
            mac="aa:aa:aa:aa:aa:aa",
            type="ether",
            link_local_addressing="no",
            lldp="no",
            emit_lldp="no",
            ipv6_accept_ra="no",
            ipv6_send_ra="no",
            vlans=["vlan1", "vlanInternet"],
        ),)

        templar = Templar(loader=None, variables=vars)
        res = templar.template(read_template_file('network.j2'))

        self.assertEqual("""
[Match]
MACAddress=aa:aa:aa:aa:aa:aa
Type=ether

[Network]
LinkLocalAddressing=no
LLDP=no
EmitLLDP=no
IPv6AcceptRA=no
IPv6SendRA=no
VLAN=vlan1
VLAN=vlanInternet
""".strip(), res.strip())
