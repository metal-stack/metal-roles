import unittest
from textwrap import dedent

from ansible.errors import AnsibleFilterError

from filter_plugins.uci import uci_batch, uci_batch_chunks, uci_batch_packages, uci_parse_export

EXPORT = dedent("""\
    package network

    config interface 'uplink'
    \toption proto 'static'
    \toption ipaddr '192.0.2.1'
    \tlist dns '198.51.100.1'
    \tlist dns '198.51.100.2'

    config switch_vlan
    \toption vlan '1'

    config switch_vlan 'vlan2'
    \toption vlan '2'

    config switch_vlan
    \toption vlan '3'

    package firewall

    config zone 'wan'
    \toption network 'wan wan2'
    \toption name 'it'\\''s'

    config rule
    \toption enabled '1'

    config rule
    \toption enabled '1'
    """)


def uplink(**options):
    base = dict(proto="static", ipaddr="192.0.2.1", dns=["198.51.100.1", "198.51.100.2"])
    base.update(options)
    return dict(network=dict(sections=dict(uplink=dict(type="interface", options=base))))


class ParseExport(unittest.TestCase):
    def test_reads_named_and_anonymous_sections_with_their_type_index(self):
        packages = uci_parse_export(EXPORT)
        vlans = [s for s in packages["network"] if s["type"] == "switch_vlan"]
        self.assertEqual([(s["name"], s["index"]) for s in vlans], [(None, 0), ("vlan2", 1), (None, 2)])

    def test_keeps_lists_apart_from_options(self):
        uplink_section = uci_parse_export(EXPORT)["network"][0]
        self.assertEqual(uplink_section["options"]["dns"], ["198.51.100.1", "198.51.100.2"])
        self.assertEqual(uplink_section["options"]["ipaddr"], "192.0.2.1")

    def test_unescapes_quotes_and_tolerates_crlf(self):
        packages = uci_parse_export(EXPORT.replace("\n", "\r\n"))
        self.assertEqual(packages["firewall"][0]["options"]["name"], "it's")


class Batch(unittest.TestCase):
    def test_matching_state_needs_no_command(self):
        self.assertEqual(uci_batch(EXPORT, uplink()), [])

    def test_changed_option_is_a_single_set(self):
        self.assertEqual(uci_batch(EXPORT, uplink(ipaddr="192.0.2.9")), ["set network.uplink.ipaddr='192.0.2.9'"])

    def test_exclusive_section_drops_undeclared_options(self):
        desired = uplink()
        del desired["network"]["sections"]["uplink"]["options"]["ipaddr"]
        self.assertEqual(uci_batch(EXPORT, desired), ["delete network.uplink.ipaddr"])

    def test_merge_section_leaves_undeclared_options(self):
        desired = dict(network=dict(sections=dict(uplink=dict(type="interface", merge=True, options=dict(proto="static")))))
        self.assertEqual(uci_batch(EXPORT, desired), [])

    def test_list_is_replaced_as_a_whole(self):
        self.assertEqual(
            uci_batch(EXPORT, uplink(dns=["198.51.100.1"])),
            ["delete network.uplink.dns", "add_list network.uplink.dns='198.51.100.1'"],
        )

    def test_space_separated_option_is_not_a_list(self):
        desired = dict(firewall=dict(sections=dict(wan=dict(type="zone", options=dict(network=["wan", "wan2"], name="it's")))))
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, desired)
        desired["firewall"]["sections"]["wan"]["options"]["name"] = "its"
        self.assertEqual(
            uci_batch(EXPORT, desired),
            [
                "delete firewall.wan.network",
                "add_list firewall.wan.network='wan'",
                "add_list firewall.wan.network='wan2'",
                "set firewall.wan.name='its'",
            ],
        )

    def test_missing_section_is_created_with_its_options(self):
        desired = dict(network=dict(sections=dict(lan9=dict(type="interface", options=dict(proto="static", dns=["192.0.2.53"])))))
        self.assertEqual(
            uci_batch(EXPORT, desired),
            ["set network.lan9=interface", "set network.lan9.proto='static'", "add_list network.lan9.dns='192.0.2.53'"],
        )

    def test_section_of_wrong_type_is_recreated(self):
        desired = dict(network=dict(sections=dict(uplink=dict(type="route", options=dict(target="192.0.2.0")))))
        self.assertEqual(
            uci_batch(EXPORT, desired),
            ["delete network.uplink", "set network.uplink=route", "set network.uplink.target='192.0.2.0'"],
        )

    def test_purge_deletes_undeclared_sections_from_the_highest_index_down(self):
        desired = dict(network=dict(purge=["switch_vlan"], sections=dict(vlan2=dict(type="switch_vlan", options=dict(vlan="2")))))
        self.assertEqual(uci_batch(EXPORT, desired), ["delete network.@switch_vlan[2]", "delete network.@switch_vlan[0]"])

    def test_purge_also_deletes_undeclared_named_sections(self):
        desired = dict(network=dict(purge=["switch_vlan"], sections=dict()))
        self.assertEqual(
            uci_batch(EXPORT, desired),
            ["delete network.@switch_vlan[2]", "delete network.vlan2", "delete network.@switch_vlan[0]"],
        )

    def test_purge_anonymous_keeps_named_sections_of_the_type(self):
        desired = dict(network=dict(purge_anonymous=["switch_vlan"], sections=dict()))
        self.assertEqual(uci_batch(EXPORT, desired), ["delete network.@switch_vlan[2]", "delete network.@switch_vlan[0]"])

    def test_indexed_section_of_an_anonymously_purged_type_fails(self):
        desired = dict(network=dict(purge_anonymous=["switch_vlan"], sections={"@switch_vlan[1]": dict(options=dict(vlan="2"))}))
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, desired)

    def test_indexed_section_merges_options(self):
        desired = dict(firewall=dict(sections={"@rule[1]": dict(options=dict(enabled=False))}))
        self.assertEqual(uci_batch(EXPORT, desired), ["set firewall.@rule[1].enabled='0'"])

    def test_indexed_section_that_does_not_exist_fails(self):
        desired = dict(firewall=dict(sections={"@rule[5]": dict(options=dict(enabled=False))}))
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, desired)

    def test_indexed_section_of_a_purged_type_fails(self):
        desired = dict(network=dict(purge=["switch_vlan"], sections={"@switch_vlan[1]": dict(options=dict(vlan="2"))}))
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, desired)

    def test_wildcard_applies_to_every_section_of_the_type(self):
        desired = dict(firewall=dict(sections={"@rule[*]": dict(options=dict(enabled="0"))}))
        self.assertEqual(
            uci_batch(EXPORT, desired),
            ["set firewall.@rule[0].enabled='0'", "set firewall.@rule[1].enabled='0'"],
        )

    def test_none_removes_an_option_even_when_merging(self):
        desired = dict(network=dict(sections=dict(uplink=dict(type="interface", merge=True, options=dict(ipaddr=None)))))
        self.assertEqual(uci_batch(EXPORT, desired), ["delete network.uplink.ipaddr"])

    def test_booleans_and_numbers_are_written_as_uci_strings(self):
        desired = dict(firewall=dict(sections={"@rule[0]": dict(options=dict(enabled=True, priority=7))}))
        self.assertEqual(uci_batch(EXPORT, desired), ["set firewall.@rule[0].priority='7'"])

    def test_package_that_was_not_exported_fails(self):
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, dict(dhcp=dict(sections=dict())))

    def test_section_type_may_contain_a_hyphen(self):
        desired = dict(network=dict(sections=dict(radio=dict(type="wifi-iface", options=dict(disabled="1")))))
        self.assertEqual(uci_batch(EXPORT, desired), ["set network.radio=wifi-iface", "set network.radio.disabled='1'"])

    def test_invalid_section_name_fails(self):
        desired = dict(network=dict(sections={"bad-name": dict(type="interface", options=dict())}))
        with self.assertRaises(AnsibleFilterError):
            uci_batch(EXPORT, desired)


class BatchChunks(unittest.TestCase):
    def test_chunks_stay_under_the_byte_budget_and_keep_the_order(self):
        batch = ["set network.s%d.o='%s'" % (i, "x" * 20) for i in range(50)]
        chunks = uci_batch_chunks(batch, 200)
        self.assertEqual([command for chunk in chunks for command in chunk], batch)
        self.assertTrue(all(sum(len(c) + 1 for c in chunk) <= 200 for chunk in chunks))
        self.assertGreater(len(chunks), 1)

    def test_command_longer_than_the_budget_fails(self):
        with self.assertRaises(AnsibleFilterError):
            uci_batch_chunks(["set network.a.b='%s'" % ("x" * 300)], 200)


class BatchPackages(unittest.TestCase):
    def test_lists_each_touched_package_once_in_order(self):
        batch = ["delete network.a", "set firewall.b.c='1'", "set network.d=interface"]
        self.assertEqual(uci_batch_packages(batch), ["network", "firewall"])


if __name__ == "__main__":
    unittest.main()
