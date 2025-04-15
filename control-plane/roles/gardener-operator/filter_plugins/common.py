from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import ipaddress
import yaml

from ansible.module_utils.six import PY3
from ansible.plugins.test.core import version_compare
from ansible.errors import AnsibleFilterError

from kubernetes import client, config


def b64decode(source):
    content = base64.b64decode(source)
    if PY3:
        content = content.decode('utf-8')
    return content


def b64encode(source):
    if PY3:
        source = source.encode('utf-8')
    content = base64.b64encode(source)
    if PY3:
        content = content.decode('utf-8')
    return content


def extract_gcp_node_network(subnets, region):
    for subnet in subnets:
        subnetwork = subnet.get("subnetwork")
        if not subnetwork:
            continue

        if region in subnetwork:
            return subnet.get("ipCidrRange")

    raise AnsibleFilterError("no node network found for region: %s" % region)

def network_cidr_add(cidr, add):
    return str(ipaddress.ip_network(cidr).network_address + add)


def gardener_managed_kubeconfig(generic_kubeconfig_secret, token_secret, server=None):
    generic_kubeconfig = yaml.safe_load(b64decode(generic_kubeconfig_secret.get("data").get("kubeconfig")))
    generic_cluster = generic_kubeconfig.get("clusters")[0].get("cluster")

    if not server:
        server = generic_cluster.get("server")

    token = yaml.safe_load(b64decode(token_secret.get("data").get("token")))

    return yaml.safe_dump({
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "name": "default-cluster",
                "cluster": {
                    "certificate-authority-data": generic_cluster.get("certificate-authority-data"),
                    "server": server,
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
                    "token": token,
                }
            }
        ],
    })


def machine_images_for_cloud_profile(image_list, cris=None):
    images = dict()
    for image in image_list:
        if 'machine' not in image.get("features", list()):
            continue

        if image.get('omit_from_cloud_profile', False):
            continue

        image_id = image.get("id")
        if image_id is None:
            continue

        parts = image_id.split("-")
        name = "-".join(parts[:-1])

        version = parts[-1]

        version_parts = version.split(".")
        # ubuntu-19.10.20200331
        # major = version_parts[0]
        minor = ".".join(version_parts[:2])

        image_versions = images.get(name, set())
        # Do not add the major version to the vector
        # metal-api cannot match latest version if only major is given
        # image_versions.add(major)
        image_versions.add(minor)
        image_versions.add(version)
        images[name] = image_versions

    result = list()
    for name, value in images.items():
        versions = list()
        for v in sorted(list(value)):
            version = dict(
                version=v
            )

            if cris is not None and name in cris:
                cri = cris[name].copy()
                cri_config = cri.pop("cris", [])
                cri_condition = cri.pop("when", None)

                if cri_condition is None:
                    version["cri"] = cri_config
                else:
                    if version_compare(v, cri_condition["version"], cri_condition["operator"]):
                        version["cri"] = cri_config

            versions.append(version)

        image = dict(
            name=name,
            versions=versions,
        )
        result.append(image)

    return result


class FilterModule(object):
    def filters(self):
        return {
            'network_cidr_add': network_cidr_add,
            'gardener_managed_kubeconfig': gardener_managed_kubeconfig,
            'machine_images_for_cloud_profile': machine_images_for_cloud_profile,
            'extract_gcp_node_network': extract_gcp_node_network,
        }
