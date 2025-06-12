# sonic-boot-to-onie

Boots a SONiC switch into ONIE so it can be reinstalled from scratch.

It depends on the `switch_facts` module from `ansible-common`, so make sure modules from `ansible-common` are included before executing this role.

## Variables

| Name                          | Mandatory | Description                                                                      |
| ----------------------------- | --------- | -------------------------------------------------------------------------------- |
| sonic_boot_to_onie_bootentry  | yes       | The efi boot entry number for the ONIE boot entry as seen with `efibootmgr`.     |
