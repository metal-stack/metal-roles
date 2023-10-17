import unittest

import yaml
import os

from ansible.template import Templar

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def read_yaml(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        return yaml.safe_load(f)


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        return f.read()


def read_template(filename):
    with open(os.path.join(TEMPLATE_DIR, filename), 'r') as f:
        return f.read()


class SonicRoleTemplates(unittest.TestCase):

    def test_exit(self):
        self._sonic_role_templates("exit")

    def test_mgmtleaf(self):
        self._sonic_role_templates("mgmtleaf")

    def test_spine(self):
        self._sonic_role_templates("spine")

    def _sonic_role_templates(self, directory):
        vars = read_yaml('../defaults/main.yaml') | read_yaml(f'./data/{directory}/input.yaml')
        templar = Templar(loader=None, variables=vars)

        self._test_metal_yaml(directory, templar)
        self._test_frr_conf(directory, templar)

        if 'sonic_extended_cacl' in vars:
            self._test_iptables_json(directory, templar)

    def _test_metal_yaml(self, directory, templar):
        expected = read_file(f'./data/{directory}/metal.yaml')
        actual = templar.template(read_template('metal.yaml.j2'))

        self.assertEqual(expected.strip(), actual.strip(), 'detected a diff for metal.yaml rendering')

    def _test_frr_conf(self, directory, templar):
        expected = read_file(f'./data/{directory}/frr.conf')
        with templar.set_temporary_context(searchpath=[TEMPLATE_DIR]):
            actual = templar.template(read_template('frr/base.j2'))

        self.assertEqual(expected.strip(), actual.strip(), 'detected a diff for frr.conf rendering')

    def _test_iptables_json(self, directory, templar):
        expected = read_file(f'./data/{directory}/iptables.json')
        actual = templar.template(read_template('iptables.json.j2'), convert_data=False)

        self.assertEqual(expected.strip(), actual.strip(), 'detected a diff for iptables.json rendering')
