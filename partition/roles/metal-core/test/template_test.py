import unittest

import yaml
import os
from textwrap import dedent

from ansible.template import Templar

from test import read_template_file


def read_defaults():
    with open(os.path.join(os.path.dirname(__file__), "..", "defaults", "main.yaml"), "r") as stream:
        return yaml.safe_load(stream)


def read_partition_defaults():
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "defaults", "defaults", "main.yaml"), "r") as stream:
        return yaml.safe_load(stream)


def base_vars():
    return read_partition_defaults() | read_defaults() | dict(
        metal_partition_timezone="Europe/Berlin",
        metal_partition_id="fra-equ01",
        metal_partition_metal_api_addr="api.metal-stack.dev",
        lo="10.0.0.11",
        asn=4200000011,
        metal_core_cidr="10.255.255.2/24",
        metal_core_rack_id="rack01",
    )


class MetalCoreEnv(unittest.TestCase):
    maxDiff = None

    def test_env_template(self):
        t = read_template_file("metal-core-env.j2")

        templar = Templar(loader=None, variables=base_vars())

        result = templar.template(t)

        self.assertEqual(dedent("""\
        TZ: "Europe/Berlin"
        METAL_CORE_LOOPBACK_IP: "10.0.0.11"
        METAL_CORE_ASN: "4200000011"
        METAL_CORE_CIDR: "10.255.255.2/24"
        METAL_CORE_PARTITION_ID: "fra-equ01"
        METAL_CORE_RACK_ID: "rack01"
        METAL_CORE_BIND_ADDRESS: 0.0.0.0
        METAL_CORE_METAL_API_IP: "api.metal-stack.dev"
        METAL_CORE_METAL_API_PORT: "443"
        METAL_CORE_METAL_API_PROTOCOL: "https"
        METAL_CORE_METAL_API_BASEPATH: "/"
        METAL_CORE_HMAC_KEY: "change-me"
        METAL_CORE_LOG_LEVEL: "warn"
        METAL_CORE_RECONFIGURE_SWITCH: "True"
        METAL_CORE_RECONFIGURE_SWITCH_INTERVAL: "10s"
        METAL_CORE_TIMEOUT: "15s"
        METAL_CORE_SET_SRC_LOOPBACK: "True"
        METAL_CORE_GRPC_ADDRESS: "api.metal-stack.dev:50051"
        METAL_CORE_GRPC_CA_CERT_FILE: "/certs/grpc/ca.pem"
        METAL_CORE_GRPC_CLIENT_CERT_FILE: "/certs/grpc/client.pem"
        METAL_CORE_GRPC_CLIENT_KEY_FILE: "/certs/grpc/client-key.pem"
        METAL_CORE_ADDITIONAL_BRIDGE_VIDS: ""
        METAL_CORE_ADDITIONAL_BRIDGE_PORTS: ""
        METAL_CORE_INTERFACES_TPL_FILE: ""
        METAL_CORE_FRR_TPL_FILE: ""
        METAL_CORE_PXE_VLAN_ID: "4000"
        """), result)

    def test_env_template_with_room_id_mgmt_gateway_and_spine_uplinks(self):
        t = read_template_file("metal-core-env.j2")

        templar = Templar(loader=None, variables=base_vars() | dict(
            metal_core_room_id="room01",
            metal_partition_mgmt_gateway="10.255.255.1",
            metal_core_spine_uplinks=["Ethernet0", "Ethernet4"],
            metal_core_additional_bridge_vids=["201-256"],
            metal_core_additional_bridge_ports=["Ethernet96", "Ethernet100"],
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        TZ: "Europe/Berlin"
        METAL_CORE_LOOPBACK_IP: "10.0.0.11"
        METAL_CORE_ASN: "4200000011"
        METAL_CORE_CIDR: "10.255.255.2/24"
        METAL_CORE_PARTITION_ID: "fra-equ01"
        METAL_CORE_RACK_ID: "rack01"
        METAL_CORE_ROOM_ID: "room01"
        METAL_CORE_BIND_ADDRESS: 0.0.0.0
        METAL_CORE_METAL_API_IP: "api.metal-stack.dev"
        METAL_CORE_METAL_API_PORT: "443"
        METAL_CORE_METAL_API_PROTOCOL: "https"
        METAL_CORE_METAL_API_BASEPATH: "/"
        METAL_CORE_HMAC_KEY: "change-me"
        METAL_CORE_LOG_LEVEL: "warn"
        METAL_CORE_RECONFIGURE_SWITCH: "True"
        METAL_CORE_RECONFIGURE_SWITCH_INTERVAL: "10s"
        METAL_CORE_TIMEOUT: "15s"
        METAL_CORE_SET_SRC_LOOPBACK: "True"
        METAL_CORE_MANAGEMENT_GATEWAY: "10.255.255.1"
        METAL_CORE_GRPC_ADDRESS: "api.metal-stack.dev:50051"
        METAL_CORE_GRPC_CA_CERT_FILE: "/certs/grpc/ca.pem"
        METAL_CORE_GRPC_CLIENT_CERT_FILE: "/certs/grpc/client.pem"
        METAL_CORE_GRPC_CLIENT_KEY_FILE: "/certs/grpc/client-key.pem"
        METAL_CORE_ADDITIONAL_BRIDGE_VIDS: "201-256"
        METAL_CORE_ADDITIONAL_BRIDGE_PORTS: "Ethernet96,Ethernet100"
        METAL_CORE_SPINE_UPLINKS: "Ethernet0,Ethernet4"
        METAL_CORE_INTERFACES_TPL_FILE: ""
        METAL_CORE_FRR_TPL_FILE: ""
        METAL_CORE_PXE_VLAN_ID: "4000"
        """), result)


class MetalCoreVolumes(unittest.TestCase):
    maxDiff = None

    def test_volumes_template_sonic(self):
        t = read_template_file("metal-core-volumes.j2")

        templar = Templar(loader=None, variables=base_vars() | dict(
            metal_stack_switch_os_is_sonic=True,
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        - /etc/sonic/:/etc/sonic
        - /var/run/redis/:/var/run/redis
        - /var/run/dbus:/var/run/dbus
        - /run/systemd/private:/run/systemd/private
        - "/certs/grpc:/certs/grpc:ro"
        - /var/run/bgp-neighbors:/var/run/bgp-neighbors"""), result)

    def test_volumes_template_cumulus_with_hosts_file_resolution_and_additional_mounts(self):
        t = read_template_file("metal-core-volumes.j2")

        templar = Templar(loader=None, variables=base_vars() | dict(
            metal_stack_switch_os_is_sonic=False,
            metal_core_consider_hosts_file_resolution=True,
            metal_core_additional_volume_mounts=["/etc/motd:/etc/motd:ro"],
        ))

        result = templar.template(t)

        self.assertEqual(dedent("""\
        - /etc/network/:/etc/network
        - /etc/frr/:/etc/frr
        - /etc/lsb-release:/etc/lsb-release:ro
        - /var/run/dbus:/var/run/dbus
        - /run/systemd/private:/run/systemd/private
        - /etc/nsswitch.conf:/etc/nsswitch.conf
        - "/certs/grpc:/certs/grpc:ro"
        - /etc/motd:/etc/motd:ro
        - /var/run/bgp-neighbors:/var/run/bgp-neighbors"""), result)
