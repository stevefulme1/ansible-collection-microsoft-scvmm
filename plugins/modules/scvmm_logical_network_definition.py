#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_network_definition
short_description: Manage SCVMM logical network definitions (network sites)
description:
  - Create, modify, and remove logical network definitions (network sites) in SCVMM.
  - Network sites define subnet and VLAN associations for host groups within a logical network.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the logical network definition (network site).
    type: str
    required: true
  state:
    description:
      - Desired state of the logical network definition.
    type: str
    choices: [present, absent]
    default: present
  logical_network:
    description:
      - Name of the logical network this definition belongs to.
    type: str
    required: true
  host_groups:
    description:
      - List of host group paths to associate with this network site.
    type: list
    elements: str
  subnet_vlans:
    description:
      - List of subnet and VLAN ID pairs for this network site.
    type: list
    elements: dict
    suboptions:
      subnet:
        description:
          - IP subnet in CIDR notation (e.g. C(192.168.1.0/24)).
        type: str
        required: true
      vlan_id:
        description:
          - VLAN ID to associate with the subnet.
        type: int
        required: true
"""

EXAMPLES = r"""
- name: Create a logical network definition
  microsoft.scvmm.scvmm_logical_network_definition:
    scvmm_server: scvmm01.example.com
    name: Corp-Site-A
    logical_network: Corp-Network
    host_groups:
      - "All Hosts\\Datacenter-A"
    subnet_vlans:
      - subnet: 192.168.1.0/24
        vlan_id: 100
      - subnet: 10.0.0.0/16
        vlan_id: 200

- name: Remove a logical network definition
  microsoft.scvmm.scvmm_logical_network_definition:
    scvmm_server: scvmm01.example.com
    name: Corp-Site-A
    logical_network: Corp-Network
    state: absent
"""

RETURN = r"""
logical_network_definition:
  description: Logical network definition details.
  returned: when state is present
  type: dict
  sample:
    name: Corp-Site-A
    logical_network: Corp-Network
"""
