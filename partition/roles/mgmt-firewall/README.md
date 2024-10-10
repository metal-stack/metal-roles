# Automatic Setup of Firewalls

This Ansible Playbook is meant to setup the Mgmtsrv firewalls automatically.
Enabling to change values inside the host_vars/router.yaml file to quickly adjust ip ranges etc.

The basic setup of the config is always the same so this can be used for every firewall.

## Known limitations:

1. Editing bridge interface to off doesnt work off lan.
2. Firewall zones arent working in LAN and WAN interfaces need to adjust manually.
3. There needs to be an inital login to change the root password to the one given in the routers.yaml
