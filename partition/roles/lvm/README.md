# lvm

Manage a servers disks with lvm.

## Variables

```yaml
# REQUIRED: The logical volumes to create. Each entry supports name, size, fstype, mountpath and optionally opts.
lvm_lvs: null
# REQUIRED: The physical disks that should be managed.
lvm_pvs: null
# REQUIRED: The volume group to be created and managed.
lvm_vg: null
```
