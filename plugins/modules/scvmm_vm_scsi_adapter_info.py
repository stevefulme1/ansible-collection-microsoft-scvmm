#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_scsi_adapter_info
short_description: Gather information about SCSI controllers on SCVMM VMs
description:
  - Retrieve details of virtual SCSI adapters attached to a virtual machine in SCVMM.
  - Returns SCSI bus number and connected disk information for each adapter.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to query SCSI adapters for.
    type: str
    required: true
  scsi_bus:
    description:
      - Specific SCSI bus number to query. Omit to list all adapters.
    type: int
"""

EXAMPLES = r"""
- name: List all SCSI adapters on a VM
  stevefulme1.scvmm.scvmm_vm_scsi_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_name: db-server-01
  register: scsi_adapters

- name: Get a specific SCSI adapter
  stevefulme1.scvmm.scvmm_vm_scsi_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_name: db-server-01
    scsi_bus: 0
  register: scsi_adapter
"""

RETURN = r"""
scsi_adapters:
  description: List of SCSI adapter dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - vm_name: db-server-01
      scsi_bus: 0
      attached_disks:
        - vhd_name: os-disk
          lun: 0
        - vhd_name: data-disk-01
          lun: 1
"""
