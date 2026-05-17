#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_network_adapter_info
short_description: Gather information about SCVMM virtual network adapters
description:
  - Retrieve detailed information about virtual network adapters (NICs) attached to VMs in SCVMM.
  - Returns MAC address, IP configuration, and VM network association details.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to retrieve adapters for.
      - Mutually exclusive with I(vm_id).
    type: str
  vm_id:
    description:
      - ID of the virtual machine to retrieve adapters for.
      - Mutually exclusive with I(vm_name).
    type: str
"""

EXAMPLES = r"""
- name: Get all network adapters for a VM by name
  microsoft.scvmm.scvmm_network_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: adapters

- name: Get all network adapters for a VM by ID
  microsoft.scvmm.scvmm_network_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_id: "12345678-abcd-1234-abcd-123456789abc"
  register: adapters
"""

RETURN = r"""
adapters:
  description: List of virtual network adapter dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Network Adapter 1
      mac_address: "00:1D:D8:B7:1C:01"
      ip_addresses:
        - 192.168.1.50
      vm_network: App-Network
      vlan_id: 100
"""
