import unittest
import sys
import yaml

from test import FILTER_PLUGINS_PATH,read_template_file,read_mock_file

from ansible.template import Templar

sys.path.insert(0, FILTER_PLUGINS_PATH)

class GardenerSoilProjectTemplate(unittest.TestCase):
    def test_gardener_soil_project_template(self):
        t = read_template_file("gardener-soil-project.yaml.j2")

        templar = Templar(loader=None, variables={
            "gardener_soil_name": "test-project",
            "gardener_soil_project_owner_name": "test-owner",
            "gardener_soil_project_members": [
                {
                    "name": "test-member1",
                    "role": "viewer",
                },
                {
                    "name": "test-member2",
                    "role": "admin",
                    "roles": [
                        "editor",
                        "owner",
                    ],
                },
            ],
            "gardener_soil_protection_enabled": "true",
        })

        res = templar.template(t)
        expected = read_mock_file("gardener_soil_project.yaml")

        self.maxDiff = None
        self.assertDictEqual(yaml.safe_load(expected), yaml.safe_load(res))
