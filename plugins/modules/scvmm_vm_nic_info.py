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
  - Retrieve details of virtual network adapters attached to a virtual machine in SCVMM.
  - Returns NIC name, connected VM network, MAC address, and MAC assignment type.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to query NICs for.
    type: str
    required: true
  name:
    description:
      - Name or slot identifier of a specific NIC. Omit to list all NICs.
    type: str
"""

EXAMPLES = r"""
- name: List all NICs on a VM
  stevefulme1.scvmm.scvmm_vm_nic_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: nics

- name: Get a specific NIC
  stevefulme1.scvmm.scvmm_vm_nic_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: NIC-1
  register: nic
"""

RETURN = r"""
nics:
  description: List of virtual NIC dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: NIC-1
      vm_name: web-server-01
      vm_network: App-Network
      mac_address: "00:1A:2B:3C:4D:5E"
      mac_type: Dynamic
      ipv4_addresses:
        - 10.0.1.10
"""
