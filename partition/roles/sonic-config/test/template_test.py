import unittest

import os
import yaml
import json
from test import read_template_file

from ansible.template import Templar

def read_yaml(f):
    with open(os.path.join(os.path.dirname(__file__), f), "r") as f:
        return yaml.safe_load(f)

def read_json(f):
    with open(os.path.join(os.path.dirname(__file__), f), "r") as f:
        return json.load(f)

def read_file(f):
    with open(os.path.join(os.path.dirname(__file__), f), "r") as f:
        return f.read()

class SonicConfigRoleTemplates(unittest.TestCase):
    def test_sonic_config_role_templates(self):
        self.maxDiff = None
        defaults = read_yaml('../defaults/main/main.yaml')
        frr_t = read_template_file('frr.conf.j2')
        iptables_t = read_template_file('iptables.json.j2')

        for tc in next(os.walk(os.path.join(os.path.dirname(__file__), 'data')))[1]:
            if tc.startswith("."):
                continue

            vars = defaults | read_yaml(f'./data/{tc}/input.yaml')
            templar = Templar(loader=None, variables=vars)

            frr_exp = read_file(f'./data/{tc}/frr.conf')
            frr_res = templar.template(frr_t)
            self.assertEqual(frr_exp.strip(), frr_res.strip(), 'frr.conf differs from the expected result')

            if 'sonic_config_extended_cacl' in vars:
                iptables_exp = read_json(f'./data/{tc}/iptables.json')
                iptables_res = templar.template(iptables_t)
                self.assertEqual(iptables_exp, iptables_res, 'iptables.json differs from the expected result')
