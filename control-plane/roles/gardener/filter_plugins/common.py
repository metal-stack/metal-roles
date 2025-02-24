from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import ipaddress
import yaml

from ansible.module_utils.six import PY3
from ansible.plugins.test.core import version_compare
from ansible.errors import AnsibleFilterError


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


def _extract_cluster_from_kubeconfig(kubeconfig_path):
    with open(kubeconfig_path, 'r') as f:
        kubeconfig = yaml.safe_load(f)

    current_context_name = kubeconfig['current-context']
    contexts = kubeconfig.get('contexts', [])
    current_contexts = [context for context in contexts if context["name"] == current_context_name]

    if not current_contexts:
        raise AnsibleFilterError("current context not found in kubeconfig")

    current_context = current_contexts[0]
    cluster_name = current_context.get("context", dict()).get("cluster")

    if not cluster_name:
        raise AnsibleFilterError("cluster name not defined in current context")

    clusters = kubeconfig.get('clusters', [])
    current_clusters = [cluster for cluster in clusters if cluster["name"] == cluster_name]

    if not current_clusters:
        raise AnsibleFilterError("current cluster not found in kubeconfig")

    return current_clusters[0].get("cluster", dict())


def kubeconfig_for_sa(kubeconfig_path, secret):
    cluster = _extract_cluster_from_kubeconfig(kubeconfig_path)

    server = cluster.get("server")

    secret_data = secret.get("data", dict())
    ca = str(secret_data.get("ca.crt"))
    token = b64decode(secret_data.get("token"))
    namespace = b64decode(secret_data.get("namespace"))

    return yaml.safe_dump({
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "name": "default-cluster",
                "cluster": {
                    "certificate-authority-data": ca,
                    "server": server,
                }
            }
        ],
        "contexts": [
            {
                "name": "default-context",
                "context": {
                    "cluster": "default-cluster",
                    "namespace": namespace,
                    "user": "default-user",
                }
            }
        ],
        "current-context": "default-context",
        "users": [
            {
                "name": "default-user",
                "user": {
                    "token": token,
                }
            }
        ],
    })


def extract_gcp_node_network(subnets, region):
    for subnet in subnets:
        subnetwork = subnet.get("subnetwork")
        if not subnetwork:
            continue

        if region in subnetwork:
            return subnet.get("ipCidrRange")

    raise AnsibleFilterError("no node network found for region: %s" % region)


def managed_seed_annotation(managed_seed_api_server, api_server=None):
    if not managed_seed_api_server:
        return ""

    settings = []

    if api_server:
        defaultReplicas = api_server.get("replicas")
        if defaultReplicas:
            settings.append("apiServer.replicas=" + str(defaultReplicas))

        autoscaler = api_server.get("autoscaler", dict())

        min_replicas = autoscaler.get("min_replicas")
        if min_replicas:
            settings.append("apiServer.autoscaler.minReplicas=" + str(min_replicas))

        max_replicas = autoscaler.get("max_replicas")
        if max_replicas:
            settings.append("apiServer.autoscaler.maxReplicas=" + str(max_replicas))

    return ",".join(settings)


def network_cidr_add(cidr, add):
    return str(ipaddress.ip_network(cidr).network_address + add)


def kubeconfig_from_cert(server, ca, cert, key, prepend_https=False):
    if prepend_https and not server.startswith("https"):
        server = "https://" + server

    return yaml.safe_dump({
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "name": "default-cluster",
                "cluster": {
                    "certificate-authority-data": b64encode(ca),
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
                    "client-certificate-data": b64encode(cert),
                    "client-key-data": b64encode(key),
                }
            }
        ],
    })


def machine_images_for_cloud_profile(image_list, cris=None, compatibilities=None):
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
                    if v in cri_condition.get("except", []):
                        pass
                    else:
                        if version_compare(v, cri_condition["version"], cri_condition["operator"]):
                            version["cri"] = cri_config

            if compatibilities is not None and name in compatibilities:
                compat = compatibilities[name].copy()

                kubelet = compat.pop("kubelet")
                condition = compat.pop("when", None)

                if condition is None:
                    version["kubeletVersionConstraint"] = kubelet
                else:
                    if v in condition.get("except", []):
                        pass
                    else:
                        if version_compare(v, condition["version"], condition["operator"]):
                            version["kubeletVersionConstraint"] = kubelet

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
            'kubeconfig_from_cert': kubeconfig_from_cert,
            'machine_images_for_cloud_profile': machine_images_for_cloud_profile,
            'kubeconfig_for_sa': kubeconfig_for_sa,
            'extract_gcp_node_network': extract_gcp_node_network,
            'managed_seed_annotation': managed_seed_annotation,
        }
