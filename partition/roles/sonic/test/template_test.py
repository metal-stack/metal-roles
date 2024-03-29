import unittest

import yaml
import os
from test import read_template_file

from ansible.template import Templar


def readYaml(f):
    with open(os.path.join(os.path.dirname(__file__), f), "r") as stream:
        return yaml.safe_load(stream)


def readFile(f):
    with open(os.path.join(os.path.dirname(__file__), f), "r") as stream:
        return stream.read()


class SonicRoleTemplates(unittest.TestCase):
    def test_sonic_role_templates(self):
        self.maxDiff = None
        defaults = readYaml('../defaults/main.yaml')
        metal_t = read_template_file('metal.yaml.j2')
        frr_t = read_template_file('frr.conf.j2')
        iptables_t = read_template_file('iptables.json.j2')

        for tc in next(os.walk(os.path.join(os.path.dirname(__file__), 'data')))[1]:
            if tc.startswith("."):
                continue

            vars = defaults | readYaml(f'./data/{tc}/input.yaml')
            templar = Templar(loader=None, variables=vars)

            metal_exp = readFile(f'./data/{tc}/metal.yaml')
            metal_res = templar.template(metal_t)
            self.assertEqual(metal_exp.strip(), metal_res.strip(), 'detected a diff for metal.yaml rendering - tc ' + tc)

            frr_exp = readFile(f'./data/{tc}/frr.conf')
            frr_res = templar.template(frr_t)
            self.assertEqual(frr_exp.strip(), frr_res.strip(), 'detected a diff for frr.conf rendering - tc ' + tc)

            if 'sonic_extended_cacl' in vars:
                iptables_exp = readFile(f'./data/{tc}/iptables.json')
                iptables_res = templar.template(iptables_t,convert_data=False)
                self.assertEqual(iptables_exp.strip(), iptables_res.strip(), 'detected a diff for iptables.json rendering - tc ' + tc)
