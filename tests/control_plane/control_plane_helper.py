from tests.ansible_helper import AnsibleTest
from tests.control_plane import PLAYBOOK_DIR, INVENTORY_DIR


class AnsibleTestControlPlane(AnsibleTest):
    def load_ansible_role(self, inventory_name, playbook_name, play_name, role_name):
        self.load(INVENTORY_DIR, inventory_name, PLAYBOOK_DIR, playbook_name, play_name, role_name)
