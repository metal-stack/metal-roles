import os

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.playbook import Playbook
from ansible.vars.hostvars import HostVars


class AnsibleTest(object):
    def __init__(self):
        self.loader = None
        self.inventory = None
        self.vars_manager = None
        self.play = None
        self.role = None

    def load(self, inventory_dir, inventory_name, playbook_dir, playbook_name, play_name, role_name):
        self.loader = DataLoader()
        self.loader.set_basedir(playbook_dir)
        self.inventory = InventoryManager(loader=self.loader, sources=os.path.join(inventory_dir, inventory_name))
        self.vars_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.play = self.get_play_by_name(playbook_name, play_name)
        self.role = self.get_role_by_name(self.play, role_name)

    def get_play_by_name(self, playbook_name, play_name):
        playbook = Playbook.load(os.path.join(self.loader.get_basedir(), playbook_name),
                                 variable_manager=self.vars_manager,
                                 loader=self.loader)
        plays = playbook.get_plays()

        play = None
        for p in plays:
            if p.get_name() == play_name:
                play = p
                break

        if play is None:
            raise Exception("no play with name %s found in plays: %s" % (play_name, plays))

        return play

    def get_role_by_name(self, play, role_name):
        roles = play.get_roles()
        for r in roles:
            if r.get_name() == role_name:
                return r
        raise Exception("no role with name %s found in roles: %s" % (role_name, roles))

    def read_role_template(self, template_name):
        path = os.path.join(self.role._role_path, "templates", template_name)
        with open(path, 'r') as f:
            return f.read()

    def get_host_vars(self, host_name):
        all_vars = self.vars_manager.get_vars(play=self.play, host=self.inventory.get_host(host_name))
        host_vars = HostVars(
            inventory=self.inventory,
            variable_manager=self.vars_manager,
            loader=self.loader,
        )
        all_vars.update(dict(hostvars=host_vars))
        return all_vars
