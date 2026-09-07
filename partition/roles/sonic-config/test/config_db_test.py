import importlib.util
import os
import unittest


def load_script(name):
    path = os.path.join(os.path.dirname(__file__), '..', 'files', name)
    spec = importlib.util.spec_from_file_location(name.removesuffix('.py'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_target_config = load_script('build_target_config.py')
check_merge_tables = load_script('check_merge_tables.py')

RUNNING = {
    'FEATURE': {'bgp': {'state': 'enabled'}},
    'SNMP_COMMUNITY': {'public': {'TYPE': 'RO'}},
    'DEVICE_METADATA': {'localhost': {'hostname': 'leaf01', 'synchronous_mode': 'enable'}},
    'PORT': {'Ethernet0': {'mtu': '9000', 'parent_port': 'Ethernet0'}},
    'INTERFACE': {'Ethernet0': {'vrf_name': 'VrfK3s'},
                  'Ethernet1': {'vrf_name': 'VrfK3s'}},
    'VLAN': {'Vlan4001': {'vlanid': '4001'}},
}

RENDERED = {
    'DEVICE_METADATA': {'localhost': {'hostname': 'leaf01'}},
    'PORT': {'Ethernet0': {'mtu': '9000'}},
    'INTERFACE': {'Ethernet1': {'vrf_name': 'VrfK3s'}},
    'VLAN': {'Vlan4001': {'vlanid': '4001'}},
}

MERGE_TABLES = {'DEVICE_METADATA', 'PORT'}


class TestBuildTargetConfig(unittest.TestCase):
    def setUp(self):
        self.target = build_target_config.build_target(RUNNING, RENDERED, MERGE_TABLES)

    def test_tables_the_role_does_not_render_are_carried_over_untouched(self):
        self.assertEqual(RUNNING['FEATURE'], self.target['FEATURE'])
        self.assertEqual(RUNNING['SNMP_COMMUNITY'], self.target['SNMP_COMMUNITY'])

    def test_keys_missing_from_a_rendered_table_are_dropped(self):
        self.assertEqual({'Ethernet1'}, set(self.target['INTERFACE']))

    def test_merged_tables_keep_the_fields_written_at_runtime(self):
        self.assertEqual({'hostname': 'leaf01', 'synchronous_mode': 'enable'},
                         self.target['DEVICE_METADATA']['localhost'])
        self.assertEqual({'mtu': '9000', 'parent_port': 'Ethernet0'},
                         self.target['PORT']['Ethernet0'])

    def test_merged_tables_take_the_rendered_value_of_a_shared_field(self):
        rendered = {'PORT': {'Ethernet0': {'mtu': '1500'}}}
        target = build_target_config.build_target(RUNNING, rendered, MERGE_TABLES)
        self.assertEqual('1500', target['PORT']['Ethernet0']['mtu'])
        self.assertEqual('Ethernet0', target['PORT']['Ethernet0']['parent_port'])

    def test_an_unmerged_table_loses_the_fields_the_render_omits(self):
        target = build_target_config.build_target(RUNNING, RENDERED, set())
        self.assertNotIn('parent_port', target['PORT']['Ethernet0'])
        self.assertNotIn('synchronous_mode', target['DEVICE_METADATA']['localhost'])


class TestCheckMergeTables(unittest.TestCase):
    def test_nothing_is_reported_when_every_partial_table_is_listed(self):
        self.assertEqual({}, check_merge_tables.find_partial_tables(RUNNING, RENDERED, MERGE_TABLES))

    def test_every_partial_table_is_reported_when_none_is_listed(self):
        findings = check_merge_tables.find_partial_tables(RUNNING, RENDERED, set())
        self.assertEqual({'DEVICE_METADATA', 'PORT'}, set(findings))

    def test_only_the_unlisted_partial_table_is_reported(self):
        findings = check_merge_tables.find_partial_tables(RUNNING, RENDERED, {'PORT'})
        self.assertEqual({'DEVICE_METADATA'}, set(findings))

    def test_the_report_names_the_fields_that_would_be_lost(self):
        findings = check_merge_tables.find_partial_tables(RUNNING, RENDERED, {'DEVICE_METADATA'})
        self.assertEqual({('parent_port',): ['Ethernet0']}, findings['PORT'])

    def test_a_fully_rendered_table_is_not_reported(self):
        findings = check_merge_tables.find_partial_tables(RUNNING, RENDERED, set())
        self.assertNotIn('VLAN', findings)
        self.assertNotIn('INTERFACE', findings)
