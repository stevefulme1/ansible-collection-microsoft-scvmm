#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_nic
short_description: Manage virtual network adapters on SCVMM VMs
description:
  - Add, modify, and remove virtual network adapters on VMs in SCVMM.
  - Connect NICs to VM networks for network connectivity.
version_added: "0.1.0"
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
  name:
    description:
      - Name or slot identifier of the virtual NIC.
    type: str
    required: true
  state:
    description:
      - Desired state of the NIC.
    type: str
    choices: [present, absent]
    default: present
  vm_network:
    description:
      - VM network to connect this NIC to.
      - Required when I(state=present).
    type: str
  mac_address:
    description:
      - Static MAC address. Omit for dynamic MAC assignment.
    type: str
  mac_type:
    description:
      - MAC address assignment type.
    type: str
    choices: [Dynamic, Static]
    default: Dynamic
"""

EXAMPLES = r"""
- name: Add a NIC to a VM
  microsoft.scvmm.scvmm_vm_nic:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: NIC-1
    vm_network: App-Network

- name: Remove a NIC from a VM
  microsoft.scvmm.scvmm_vm_nic:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: NIC-1
    state: absent
"""

RETURN = r"""
nic:
  description: Virtual NIC details.
  returned: when state is present
  type: dict
  sample:
    name: NIC-1
    vm_network: App-Network
    mac_address: "00:1A:2B:3C:4D:5E"
    mac_type: Dynamic
"""
