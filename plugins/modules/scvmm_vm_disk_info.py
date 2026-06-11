#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_disk_info
short_description: Gather information about virtual hard disk attachments on SCVMM VMs
description:
  - Retrieve details of virtual hard disks attached to virtual machines in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  vhd_name:
    description:
      - Name of a specific virtual hard disk. Omit to list all disks attached to the VM.
    type: str
"""

EXAMPLES = r"""
- name: List all disks attached to a VM
  stevefulme1.scvmm.scvmm_vm_disk_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: vm_disks

- name: Get details of a specific disk attachment
  stevefulme1.scvmm.scvmm_vm_disk_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    vhd_name: data-disk-01
  register: disk_info

- name: List VM disks using WinRM credentials
  stevefulme1.scvmm.scvmm_vm_disk_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
    vm_name: web-server-01
  register: vm_disks
"""

RETURN = r"""
disks:
  description: List of disk attachment dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    vm_name:
      description: Name of the virtual machine.
      type: str
    vhd_name:
      description: Name of the virtual hard disk.
      type: str
    bus_type:
      description: Bus type for the disk attachment.
      type: str
    bus:
      description: Bus number for the disk.
      type: int
    lun:
      description: LUN number for the disk on the specified bus.
      type: int
    size_gb:
      description: Size of the disk in GB.
      type: int
    path:
      description: Full path to the VHD file.
      type: str
"""
