# metal-roles

This repository contains Ansible roles for deploying metal-stack. It does not contain any specific playbooks.

The metal-stack primarily consists of a control plane and partitions that register at the control plane. For this reason, the roles in this repository are divided into two separate folders, one containing roles relevant for the control plane and another directory containing roles for bootstrapping a partition. Please find more documentation in the respective sub folders:

- [Control Plane Deployment](control-plane)
- [Partition Deployment](partition)

## Usage

It's convenient to use ansible-galaxy in order to use this project. The roles of this repository depend on roles, modules and plugins of the project [ansible-common](https://github.com/metal-stack/ansible-common).

For your deployment project, set up a `requirements.yml`:

```yaml
- src: https://github.com/metal-stack/ansible-common.git
  name: ansible-common
  version: master # use release versions if you want to have stable deployment!
- src: https://github.com/metal-stack/metal-roles.git
  name: metal-roles
  version: master # use release versions if you want to have stable deployment!

# you can find release versions here: https://github.com/metal-stack/releases
```

You can then download the roles with the following command:

```bash
ansible-galaxy install -r requirements.yml
```

An example for how to use this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.

## Resolving Image Versions

## Resolving Image Versions

Many roles require names and tags of the microservices to be set explicitly. You can, however, make use of the [setup_yaml](https://github.com/metal-stack/ansible-common/blob/master/library/setup_yaml.py) module, which fetches image release versions from the [release](https://github.com/metal-stack/releases) vector. This way, you only need to define the following data structure somewhere in your playbooks:

```yaml
setup_yaml:
  - url: https://raw.githubusercontent.com/metal-stack/releases/master/release.yaml
    meta_var: metal_stack_release
    # the metal_stack_release variable is provided through role defaults of this project
    # use release versions if you want to have stable deployment!
```
