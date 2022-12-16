import unittest

from test import read_template_file

from ansible.template import Templar


class SSHAccess(unittest.TestCase):
    def test_ssh_config_template(self):
        t = read_template_file("ssh_config.j2")

        templar = Templar(loader=None, variables=dict(
            groups={"a": ["host-a", "host-b"], "b": ["host-c"]},
            hostvars={
                "host-a": {"ansible_hostname": "a", "ansible_user": "metal"},
                "host-b": {"ansible_hostname": "b", "ansible_user": "metal"},
            },
            ssh_access_group_name="a",
        ))

        res = templar.template(t)

        self.assertIn(res.strip(), """
Host a
    User metal
    HostName a
    IdentityFile ~/.ssh/id_rsa
Host b
    User metal
    HostName b
    IdentityFile ~/.ssh/id_rsa
        """.strip())
