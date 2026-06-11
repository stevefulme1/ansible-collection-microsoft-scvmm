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
  - Retrieve details of virtual SCSI adapters on virtual machines in SCVMM.
version_added: "0.2.0"
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
"""

EXAMPLES = r"""
- name: List all SCSI adapters on a VM
  stevefulme1.scvmm.scvmm_vm_scsi_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_name: db-server-01
  register: scsi_adapters

- name: List SCSI adapters using WinRM credentials
  stevefulme1.scvmm.scvmm_vm_scsi_adapter_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
    vm_name: db-server-01
  register: scsi_adapters
"""

RETURN = r"""
scsi_adapters:
  description: List of SCSI adapter dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    vm_name:
      description: Name of the virtual machine.
      type: str
    scsi_bus:
      description: SCSI bus number for the adapter.
      type: int
    adapter_type:
      description: Type of SCSI adapter.
      type: str
    max_luns:
      description: Maximum number of LUNs supported.
      type: int
"""
