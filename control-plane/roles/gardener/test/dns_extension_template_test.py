import unittest
import sys
import yaml

from ansible.template import Templar
from test import read_template_file
from unittest.mock import patch, MagicMock

class ShootDnsExtensionControllerDeploymentTemplate(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_shoot_dns_extension_controller_deployment_template(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '''
---
apiVersion: core.gardener.cloud/v1beta1
kind: ControllerDeployment
metadata:
  name: extension-shoot-dns-service
type: helm
providerConfig:
  chart: a-chart
  values:
    image:
      tag: v1.48.0
'''
        mock_urlopen.return_value = cm

        t = read_template_file("shoot-dns-service/controller-deployment.yaml")

        templar = Templar(loader=None, variables={
            "gardener_shoot_dns_service_image_tag": "v0.0.1",
            "gardener_shoot_dns_service_repo_ref": "gardener/gardener-extension-shoot-dns-service/{{ gardener_shoot_dns_service_image_tag }}",
            "gardener_shoot_dns_service_image_name": "extension-image",
            "gardener_shoot_dns_service_image_tag": "extension-tag",
            "gardener_shoot_dns_service_image_vector_overwrite": [
                {
                    "name": "dns-controller-manager",
                    "sourceRepository": "github.com/gardener/external-dns-management",
                    "repository": "europe-docker.pkg.dev/gardener-project/public/dns-controller-manager",
                    "tag": "0.7.1",
                },
            ],
            "gardener_shoot_dns_service_dns_controller_manager_image_name": "dns-controller-image",
            "gardener_shoot_dns_service_dns_controller_manager_image_tag": "dns-controller-tag",
        })


        res = templar.template(t)

        expected = '''
---
apiVersion: core.gardener.cloud/v1beta1
kind: ControllerDeployment
metadata:
  name: extension-shoot-dns-service
type: helm
providerConfig:
  chart: "a-chart"
  values:
    image:
      repository: "extension-image"
      tag: "extension-tag"
    imageVectorOverwrite: |
      images:
        - name: dns-controller-manager
          repository: europe-docker.pkg.dev/gardener-project/public/dns-controller-manager
          sourceRepository: github.com/gardener/external-dns-management
          tag: 0.7.1
    dnsProviderManagement:
      enabled: true
    dnsControllerManager:
      deploy: true
      image:
        tag: "dns-controller-tag"
        repository: "dns-controller-image"
'''

        self.maxDiff = None
        self.assertDictEqual(yaml.safe_load(expected), yaml.safe_load(res))
