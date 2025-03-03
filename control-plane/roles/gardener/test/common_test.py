from mock import patch, mock_open
import json
import sys
import unittest
import yaml

from test import FILTER_PLUGINS_PATH, read_mock_file

sys.path.insert(0, FILTER_PLUGINS_PATH)
from common import kubeconfig_from_cert, network_cidr_add, machine_images_for_cloud_profile, kubeconfig_for_sa, extract_gcp_node_network, managed_seed_annotation


class KubeconfigTest(unittest.TestCase):
    def test_kubeconfig_from_cert(self):
        actual = kubeconfig_from_cert("1.2.3.4", "ca", "cert", "key")

        self.maxDiff = None

        expected = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": "default-cluster",
                    "cluster": {
                        "certificate-authority-data": "Y2E=",
                        "server": "1.2.3.4",
                    }
                }
            ],
            "current-context": "default-context",
            "contexts": [
                {
                    "name": "default-context",
                    "context": {
                        "cluster": "default-cluster",
                        "user": "default-user",
                    }
                }
            ],
            "users": [
                {
                    "name": "default-user",
                    "user": {
                        "client-certificate-data": "Y2VydA==",
                        "client-key-data": "a2V5",
                    }
                }
            ],
        }

        self.assertDictEqual(expected, yaml.safe_load(actual))

    def test_kubeconfig_from_cert_prepend_https(self):
        actual = kubeconfig_from_cert("1.2.3.4", "ca", "cert", "key", prepend_https=True)

        self.maxDiff = None

        expected = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": "default-cluster",
                    "cluster": {
                        "certificate-authority-data": "Y2E=",
                        "server": "https://1.2.3.4",
                    }
                }
            ],
            "current-context": "default-context",
            "contexts": [
                {
                    "name": "default-context",
                    "context": {
                        "cluster": "default-cluster",
                        "user": "default-user",
                    }
                }
            ],
            "users": [
                {
                    "name": "default-user",
                    "user": {
                        "client-certificate-data": "Y2VydA==",
                        "client-key-data": "a2V5",
                    }
                }
            ],
        }

        self.assertDictEqual(expected, yaml.safe_load(actual))


class NetworkTest(unittest.TestCase):
    def test_network_cidr_add(self):
        actual = network_cidr_add("10.0.0.0/28", 20)
        expected = "10.0.0.20"

        self.assertEqual(actual, expected)


class ImageTest(unittest.TestCase):
    def test_image_list(self):
        self.maxDiff = None

        sample_data = """
        - id: firewall-ubuntu-2.0.20200714
          name: Firewall 2 Ubuntu 20200714
          description: Firewall 2 Ubuntu 20200714
          url: http://images.metal-stack.io/metal-os/master/firewall/2.0-ubuntu/20200714/img.tar.lz4
          features:
            - firewall
            - machine
        - id: firewall-2.0.20200714
          name: Firewall 2 Debian 20200714
          description: Firewall 2 Debian 20200714
          url: http://images.metal-stack.io/metal-os/master/firewall/2.0/20200714/img.tar.lz4
          features:
            - firewall
        - id: ubuntu-19.10.20200331
          name: Ubuntu 19.10 20200331
          description: Ubuntu 19.10 20200331
          url: http://images.metal-stack.io/metal-os/ubuntu/19.10/20200331/img.tar.lz4
          features:
            - machine
        - id: ubuntu-19.10.20200701
          name: Ubuntu 19.10 20200701
          description: Ubuntu 19.10 20200701
          url: http://images.metal-stack.io/metal-os/ubuntu/19.10/20200701/img.tar.lz4
          features:
            - machine
        - id: ubuntu-20.04.20200331
          name: Ubuntu 20.04 20200331
          description: Ubuntu 20.04 20200331
          url: http://images.metal-stack.io/metal-os/ubuntu/20.04/20200331/img.tar.lz4
          features:
            - machine
        - id: debian-10.0.20200331
          name: Debian 10.0.20200331
          description: Debian 10 20200331
          url: http://images.metal-stack.io/metal-os/debian/10/20200331/img.tar.lz4
          features:
            - machine
        - id: centos-7.0.20210620
          name: Centos 7 20210620
          description: Centos 7 20210620
          url: http://images.metal-stack.io/metal-os/master/centos/7/20210620/img.tar.lz4
          omit_from_cloud_profile: yes
          features:
              - machine
        """
        actual = machine_images_for_cloud_profile(yaml.safe_load(sample_data))
        expected = [
            {
                "name": "firewall-ubuntu",
                "versions": [
                    {"version": "2.0"},
                    {"version": "2.0.20200714"},
                ]
            },
            {
                "name": "ubuntu",
                "versions": [
                    {"version": "19.10"},
                    {"version": "19.10.20200331"},
                    {"version": "19.10.20200701"},
                    {"version": "20.04"},
                    {"version": "20.04.20200331"},
                ],
            },
            {
                "name": "debian",
                "versions": [
                    {"version": "10.0"},
                    {"version": "10.0.20200331"},
                ],
            },
        ]

        self.assertListEqual(actual, expected)

    def test_image_list_with_cri_mapping(self):
        self.maxDiff = None

        sample_data = """
        - id: firewall-ubuntu-2.0.20200714
          name: Firewall 2 Ubuntu 20200714
          description: Firewall 2 Ubuntu 20200714
          url: http://images.metal-stack.io/metal-os/master/firewall/2.0-ubuntu/20200714/img.tar.lz4
          features:
            - firewall
            - machine
        - id: firewall-2.0.20200714
          name: Firewall 2 Debian 20200714
          description: Firewall 2 Debian 20200714
          url: http://images.metal-stack.io/metal-os/master/firewall/2.0/20200714/img.tar.lz4
          features:
            - firewall
        - id: ubuntu-19.10.20200331
          name: Ubuntu 19.10 20200331
          description: Ubuntu 19.10 20200331
          url: http://images.metal-stack.io/metal-os/ubuntu/19.10/20200331/img.tar.lz4
          features:
            - machine
        - id: ubuntu-19.10.20200701
          name: Ubuntu 19.10 20200701
          description: Ubuntu 19.10 20200701
          url: http://images.metal-stack.io/metal-os/ubuntu/19.10/20200701/img.tar.lz4
          features:
            - machine
        - id: ubuntu-20.04.20200331
          name: Ubuntu 20.04 20200331
          description: Ubuntu 20.04 20200331
          url: http://images.metal-stack.io/metal-os/ubuntu/20.04/20200331/img.tar.lz4
          features:
            - machine
        """

        cris = [
            {
                "name": "containerd",
                "containerRuntimes": [
                    {"type": "gvisor"},
                    {"type": "kata-containers"},
                ],
            }
        ]
        cri_mapping = {
            "ubuntu": {
                "when": {
                    "operator": ">=",
                    "version": "20.04",
                },
                "cris": cris,
            }
        }

        actual = machine_images_for_cloud_profile(yaml.safe_load(sample_data), cris=cri_mapping)
        expected = [
            {
                "name": "firewall-ubuntu",
                "versions": [
                    {"version": "2.0"},
                    {"version": "2.0.20200714"},
                ]
            },
            {
                "name": "ubuntu",
                "versions": [
                    {"version": "19.10"},
                    {"version": "19.10.20200331"},
                    {"version": "19.10.20200701"},
                    {
                        "version": "20.04",
                        "cri": [
                            {
                                "name": "containerd",
                                "containerRuntimes": [
                                    {"type": "gvisor"},
                                    {"type": "kata-containers"},
                                ],
                            }
                        ],
                    },
                    {
                        "version": "20.04.20200331",
                        "cri": [
                            {
                                "name": "containerd",
                                "containerRuntimes": [
                                    {"type": "gvisor"},
                                    {"type": "kata-containers"},
                                ],
                            }
                        ],
                    },
                ],
            },
        ]

        self.assertListEqual(actual, expected)


    def test_image_list_with_compatibility_mapping(self):
        self.maxDiff = None

        sample_data = """
        - id: debian-12.0.20240101
          name: Debian 12 20240101
          description: Debian 12 20240101
          url: http://images.metal-stack.io/metal-os/debian/12/img.tar.lz4
          features:
            - machine
        - id: debian-12.0.20250231
          name: Debian 12 20250231
          description: Debian 12 20250231
          url: http://images.metal-stack.io/metal-os/debian/12/img.tar.lz4
          features:
            - machine
        """

        compat_mapping = {
            "debian": {
                "when": {
                    "operator": "<",
                    "version": "12.0.20250101",
                    "except": ["12.0"],
                },
                "kubelet": "<= 1.30",
            }
        }

        actual = machine_images_for_cloud_profile(yaml.safe_load(sample_data), compatibilities=compat_mapping)
        expected = [
            {
                "name": "debian",
                "versions": [
                    {
                        "version": "12.0",
                    },
                    {
                        "version": "12.0.20240101",
                        "kubeletVersionConstraint": "<= 1.30"
                    },
                    {
                        "version": "12.0.20250231",
                    },
                ],
            },
        ]

        self.assertListEqual(actual, expected)


class KubeconfigTest(unittest.TestCase):
    def test_kubeconfig_for_sa(self):
        kubeconfig = read_mock_file("kubeconfig.yaml")
        secret = json.loads(read_mock_file("secret.json"))

        with patch("builtins.open", mock_open(read_data=kubeconfig)) as mock_file:
            actual = kubeconfig_for_sa("~/.kube/config", secret)

        self.maxDiff = None

        expected = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": "default-cluster",
                    "cluster": {
                        "certificate-authority-data": "Y2VydA==",
                        "server": "https://api-server-test.de",
                    }
                }
            ],
            "contexts": [
                {
                    "name": "default-context",
                    "context": {
                        "cluster": "default-cluster",
                        "namespace": "garden",
                        "user": "default-user",
                    }
                }
            ],
            "current-context": "default-context",
            "users": [
                {
                    "name": "default-user",
                    "user": {
                        "token": "token",
                    }
                }
            ],
        }

        self.assertDictEqual(expected, yaml.safe_load(actual))


class GCPTest(unittest.TestCase):
    def test_extract_gcp_node_network(self):
        subnets = json.loads(read_mock_file("gke_container_subnets.json"))

        actual = extract_gcp_node_network(subnets, "europe-west3")

        self.assertEqual("0.0.0.3/32", actual)


class ShootedSeedTest(unittest.TestCase):
    def test_managed_seed_annotation_no_shooted_seed(self):
        actual = managed_seed_annotation(False)

        self.assertEqual("", actual)

    def test_managed_seed_api_server_configs(self):
        actual = managed_seed_annotation(True, api_server=dict(autoscaler=dict(min_replicas=2, max_replicas=2)))

        self.assertEqual("apiServer.autoscaler.minReplicas=2,apiServer.autoscaler.maxReplicas=2", actual)

    def test_managed_seed_api_server_configs_with_default_replicas(self):
        actual = managed_seed_annotation(True, api_server=dict(replicas=2,autoscaler=dict(min_replicas=2, max_replicas=2)))

        self.assertEqual("apiServer.replicas=2,apiServer.autoscaler.minReplicas=2,apiServer.autoscaler.maxReplicas=2", actual)
