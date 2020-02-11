import os
import subprocess
import unittest

from tests.control_plane.control_plane_helper import AnsibleTestControlPlane
from ansible.module_utils.six import b


class Metal(unittest.TestCase, AnsibleTestControlPlane):
    def test_metal_helm_chart_compiles(self):
        self.load_ansible_role("inventory.yaml", "cp.yaml", "deploy control plane", "metal-roles/control-plane/roles/metal")

        chart_path = os.path.join(self.role._role_path, "files", "metal-control-plane")

        out = subprocess.check_output(["helm", "lint", chart_path])

        self.assertIn(b("0 chart(s) failed"), out)
