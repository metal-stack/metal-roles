# metal-roles

This repository contains Ansible roles for deploying Metal Stack. It does not contain any specific playbooks.

The Metal Stack primarily consists of a control plane and partitions that register at the control plane. For this reason, the roles in this repository are divided into two separate folders, one containing roles relevant for the control plane and another directory containing roles for bootstrapping a partition. Please find more documentation in the respective sub folders:

- [Control Plane Deployment](control-plane)
- [Partition Deployment](partition)

## Usage

It's convenient to use ansible-galaxy in order to use this project. The roles of this repository depend on roles, modules and plugins of the project [ansible-common](https://github.com/metal-stack/ansible-common).

For your deployment project, set up a `requirements.yml`:

```yaml
- src: https://github.com/metal-stack/ansible-common.git
  name: ansible-common
  version: v0.4.0
- src: https://github.com/metal-stack/metal-roles.git
  name: metal-roles
  version: v0.1.0
```

You can then download the roles with the following command:

```bash
ansible-galaxy install -r requirements.yml
```

An example for how to use this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.
