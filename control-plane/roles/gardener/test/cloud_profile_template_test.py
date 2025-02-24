import unittest
import sys
import yaml

from test import FILTER_PLUGINS_PATH,read_template_file, read_mock_file

from ansible.template import Templar


sys.path.insert(0, FILTER_PLUGINS_PATH)
from common import machine_images_for_cloud_profile


class CloudProfileTemplate(unittest.TestCase):
    def test_cloud_profile_template_template(self):
        t = read_template_file("30-cloud-profile-metal.yaml")

        templar = Templar(loader=None, variables={
            "gardener_cloud_profile_stage_name": "prod",
            "gardener_cloud_profile_metal_api_url": "https://metal-api",
            "gardener_cloud_profile_metal_api_hmac": "hmac",
            "gardener_cloud_profile_machine_images": [
                {
                    "id": "ubuntu-20.04.20210131",
                    "name": "Ubuntu 20.04 20210131",
                    "description": "Ubuntu 20.04 20210131",
                    "url": "http://images.metal-stack.io/metal-os/ubuntu",
                    "features": ["machine"],
                },
                {
                    "id": "firewall-ubuntu-3.0.20300101",
                    "name": "Firewall Ubuntu 3.0 20300101",
                    "description": "Firewall Ubuntu 3.0 20300101",
                    "url": "http://images.metal-stack.io/metal-os/firewall",
                    "features": ["firewall"],
                },
            ],
            "gardener_cloud_profile_firewall_images": [
                "firewall-ubuntu-3.0",
            ],
            "gardener_cloud_profile_firewall_images_from_machine_images": True,
            "gardener_cloud_profile_firewall_controller_versions": [
                {
                    "classification": "supported",
                    "url": "https://images.metal-stack.io/firewall-controller/v2.0.4/firewall-controller",
                    "version": "v2.0.4",
                },
            ],
            "gardener_cloud_profile_kubernetes": {
                "versions": [
                    {
                        "version": "1.18.0",
                        "expirationDate": "2020-12-01T00:00:00Z",
                    },
                    {
                        "version": "1.24.15",
                    },
                ],
            },
            "gardener_cloud_profile_machine_types": [
                {
                    "architecture": "amd64",
                    "cpu": "8",
                    "gpu": "0",
                    "memory": "32Gi",
                    "name": "n1-medium-x86",
                    "usable": True,
                },
            ],
            "gardener_cloud_profile_regions": [
                {
                    "name": "a",
                    "zones": [
                        {"name": "partition-a"}
                    ],
                },
            ],
            "gardener_cloud_profile_partitions": {
                "partition-a": {
                    "default-machine-types": {
                        "firewall": ["n1-medium-x86"],
                    },
                },
            },
            "gardener_os_cri_mapping": {
                "ubuntu": {
                    "when": None,
                    "cris": [{"name": "containerd"}],
                    "containerRuntimes": [],
                },
            },
            "gardener_os_compatibility_mapping": {},
        })

        templar.environment.filters["machine_images_for_cloud_profile"] = machine_images_for_cloud_profile

        res = templar.template(t)

        expected = read_mock_file("cloudprofile.yaml")

        self.maxDiff = None
        self.assertDictEqual(yaml.safe_load(expected), yaml.safe_load(res))
