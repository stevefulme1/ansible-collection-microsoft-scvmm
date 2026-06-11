#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_nic_info
short_description: Gather information about virtual network adapters on SCVMM VMs
description:
  - Retrieve details of virtual network adapters on virtual machines in SCVMM.
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
  name:
    description:
      - Name or slot identifier of a specific virtual NIC. Omit to list all NICs on the VM.
    type: str
"""

EXAMPLES = r"""
- name: List all NICs on a VM
  stevefulme1.scvmm.scvmm_vm_nic_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: vm_nics

- name: Get details of a specific NIC
  stevefulme1.scvmm.scvmm_vm_nic_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: NIC-1
  register: nic_info

- name: List VM NICs using WinRM credentials
  stevefulme1.scvmm.scvmm_vm_nic_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
    vm_name: web-server-01
  register: vm_nics
"""

RETURN = r"""
nics:
  description: List of virtual NIC dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    name:
      description: Name or slot identifier of the virtual NIC.
      type: str
    vm_network:
      description: VM network this NIC is connected to.
      type: str
    mac_address:
      description: MAC address of the NIC.
      type: str
    mac_type:
      description: MAC address assignment type.
      type: str
    enabled:
      description: Whether the NIC is enabled.
      type: bool
    connected:
      description: Whether the NIC is connected.
      type: bool
"""
