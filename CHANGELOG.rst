==========================================
Microsoft SCVMM Collection Release Notes
==========================================

.. contents:: Topics

v0.1.0
======

Release Summary
----------------

Initial release of the Microsoft SCVMM collection for Ansible.
Provides 26 modules for managing SCVMM infrastructure via
PowerShell over WinRM or SSH.

Major Changes
-------------

- Initial collection scaffold with GPL-3.0-or-later license.
- Requires ansible-core >= 2.16.0 and Python >= 3.12.
- Supports both WinRM and SSH connection methods.
- Zero collection dependencies — only requires pywinrm or pypsrp on the controller and the VirtualMachineManager PowerShell module on the target host.

Minor Changes
-------------

- scvmm_vm — Create, modify, and remove virtual machines.
- scvmm_vm_info — Gather information about virtual machines.
- scvmm_vm_state — Manage VM power state (start, stop, suspend, resume).
- scvmm_vm_checkpoint — Manage VM checkpoints (create, delete, restore).
- scvmm_vm_checkpoint_info — Gather information about VM checkpoints.
- scvmm_vm_disk — Attach and detach virtual hard disks to VMs.
- scvmm_vm_nic — Manage virtual network adapters on VMs.
- scvmm_template — Create, modify, and remove VM templates.
- scvmm_template_info — Gather information about VM templates.
- scvmm_cloud — Create, modify, and remove SCVMM clouds.
- scvmm_cloud_info — Gather information about SCVMM clouds.
- scvmm_host_group — Manage host groups.
- scvmm_host_group_info — Gather information about host groups.
- scvmm_host_info — Gather information about Hyper-V hosts.
- scvmm_logical_network — Create, modify, and remove logical networks.
- scvmm_logical_network_info — Gather information about logical networks.
- scvmm_vm_network — Create, modify, and remove VM networks.
- scvmm_vm_network_info — Gather information about VM networks.
- scvmm_ip_pool — Manage static IP address pools.
- scvmm_port_classification — Manage port classifications.
- scvmm_virtual_hard_disk — Create and remove virtual hard disks (VHD/VHDX).
- scvmm_virtual_hard_disk_info — Gather information about virtual hard disks.
- scvmm_storage_classification — Manage storage classifications.
- scvmm_library_server_info — Gather information about library servers.
- scvmm_user_role — Manage user roles (RBAC).
- scvmm_user_role_info — Gather information about user roles.
