#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_subnet
short_description: Manage SCVMM VM subnets
description:
  - Create, modify, and remove VM subnets in SCVMM.
  - VM subnets define IP address spaces within a VM network.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the VM subnet.
    type: str
    required: true
  state:
    description:
      - Desired state of the VM subnet.
    type: str
    choices: [present, absent]
    default: present
  vm_network:
    description:
      - Name of the VM network this subnet belongs to.
    type: str
    required: true
  subnet:
    description:
      - IP subnet in CIDR notation (e.g. C(192.168.1.0/24)).
      - Required when I(state=present).
    type: str
"""

EXAMPLES = r"""
- name: Create a VM subnet
  microsoft.scvmm.scvmm_vm_subnet:
    scvmm_server: scvmm01.example.com
    name: App-Subnet
    vm_network: App-Network
    subnet: 10.10.1.0/24

- name: Remove a VM subnet
  microsoft.scvmm.scvmm_vm_subnet:
    scvmm_server: scvmm01.example.com
    name: App-Subnet
    vm_network: App-Network
    state: absent
"""

RETURN = r"""
vm_subnet:
  description: VM subnet details.
  returned: when state is present
  type: dict
  sample:
    name: App-Subnet
    vm_network: App-Network
    subnet: 10.10.1.0/24
"""
