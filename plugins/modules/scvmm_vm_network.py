#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_network
short_description: Manage SCVMM VM networks
description:
  - Create, modify, and remove VM networks in SCVMM.
  - VM networks are tenant-facing abstractions of logical networks.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the VM network.
    type: str
    required: true
  state:
    description:
      - Desired state of the VM network.
    type: str
    choices: [present, absent]
    default: present
  logical_network:
    description:
      - Name of the logical network this VM network is bound to.
      - Required when I(state=present).
    type: str
  description:
    description:
      - Description of the VM network.
    type: str
  isolation_type:
    description:
      - Network isolation type.
    type: str
    choices: [NoIsolation, VLANNetwork, WindowsNetworkVirtualization]
    default: NoIsolation
"""

EXAMPLES = r"""
- name: Create a VM network bound to the production logical network
  stevefulme1.scvmm.scvmm_vm_network:
    scvmm_server: scvmm01.example.com
    name: Production VLAN
    logical_network: Management Network
    description: Production workload network
    isolation_type: VLANNetwork

- name: Create a VM network with no isolation for dev workloads
  stevefulme1.scvmm.scvmm_vm_network:
    scvmm_server: scvmm01.example.com
    name: Dev-Network
    logical_network: Management Network
    description: Development environment network
    isolation_type: NoIsolation

- name: Remove a VM network
  stevefulme1.scvmm.scvmm_vm_network:
    scvmm_server: scvmm01.example.com
    name: Dev-Network
    state: absent
"""

RETURN = r"""
vm_network:
  description: VM network details.
  returned: when state is present
  type: dict
"""
