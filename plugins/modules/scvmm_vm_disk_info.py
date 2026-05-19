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
  - Retrieve details of virtual hard disks attached to a virtual machine in SCVMM.
  - Returns bus type, bus number, and LUN assignment for each attached disk.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to query disk attachments for.
    type: str
    required: true
  vhd_name:
    description:
      - Name of a specific virtual hard disk. Omit to list all attached disks.
    type: str
"""

EXAMPLES = r"""
- name: List all disk attachments on a VM
  stevefulme1.scvmm.scvmm_vm_disk_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: disks

- name: Get a specific disk attachment
  stevefulme1.scvmm.scvmm_vm_disk_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    vhd_name: data-disk-01
  register: disk
"""

RETURN = r"""
disk_attachments:
  description: List of virtual hard disk attachment dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - vm_name: web-server-01
      vhd_name: data-disk-01
      bus_type: SCSI
      bus: 0
      lun: 1
      size_gb: 100
      vhd_type: Dynamic
"""
