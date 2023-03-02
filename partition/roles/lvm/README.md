# lvm

Manage a servers disks with lvm.

## Variables

| Name              | Mandatory | Description                                             |
|-------------------|-----------|---------------------------------------------------------|
| lvm_vg            | yes       | the volume group to be created and managed.             |
| lvm_pvs           | yes       | the physical disks that should be managed.              |
| lvm_lvs           | yes       | the logical volumes that should be created as array.    |
| lvm_lvs.name      | yes       | the name of the logical volume.                         |
| lvm_lvs.size      | yes       | the size of the logical volume.                         |
| lvm_lvs.fstype    | yes       | the filesystem of the logical volume.                   |
| lvm_lvs.mountpath | yes       | the path where the logical volume should be mounted to. |
| lvm_lvs.opts      |           | the options when creating this logibal volume.          |

```yaml
lvm_vg: metal
lvm_pvs:
- /dev/nvme0n1
- /dev/nvme1n1
lvm_lvs:
- name: image-cache
  size: 150G
  fstype: ext4
  mountpath: /metal-image-cache-sync
  opts: --mirrors 1 --type raid1 --nosync
```