#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_scsi_adapter
short_description: Manage SCSI controllers on SCVMM virtual machines
description:
  - Add and remove virtual SCSI adapters on virtual machines in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  state:
    description:
      - Desired state of the SCSI adapter.
    type: str
    choices: [present, absent]
    default: present
  scsi_bus:
    description:
      - SCSI bus number for the adapter.
      - Used to identify a specific adapter when removing.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Add a SCSI controller to a VM
  microsoft.scvmm.scvmm_vm_scsi_adapter:
    scvmm_server: scvmm01.example.com
    vm_name: db-server-01
    scsi_bus: 1

- name: Remove a SCSI controller from a VM
  microsoft.scvmm.scvmm_vm_scsi_adapter:
    scvmm_server: scvmm01.example.com
    vm_name: db-server-01
    state: absent
    scsi_bus: 1
"""

RETURN = r"""
scsi_adapter:
  description: Details of the SCSI adapter.
  returned: when state is present
  type: dict
  sample:
    vm_name: db-server-01
    scsi_bus: 1
changed:
  description: Whether the SCSI adapter was created or removed.
  returned: always
  type: bool
"""
