from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


def managed_seed_api_server_annotation(api_server=dict()):
    settings = []

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


class FilterModule(object):
    def filters(self):
        return {
            'managed_seed_api_server_annotation': managed_seed_api_server_annotation,
        }
