#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_uplink_port_profile
short_description: Manage SCVMM native uplink port profiles
description:
  - Create, modify, and remove native uplink port profiles in SCVMM.
  - Uplink port profiles define NIC teaming and load balancing for host adapters.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the uplink port profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the uplink port profile.
    type: str
    choices: [present, absent]
    default: present
  load_balancing_algorithm:
    description:
      - Load balancing algorithm for the uplink port profile.
    type: str
    choices:
      - HostDefault
      - HyperVPort
      - Dynamic
      - TransportPorts
      - IPAddresses
      - MACAddresses
  logical_network_definitions:
    description:
      - List of logical network definition names to associate with this uplink port profile.
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: Create an uplink port profile
  microsoft.scvmm.scvmm_uplink_port_profile:
    scvmm_server: scvmm01.example.com
    name: Corp-Uplink
    load_balancing_algorithm: Dynamic
    logical_network_definitions:
      - Corp-Site-A
      - Corp-Site-B

- name: Remove an uplink port profile
  microsoft.scvmm.scvmm_uplink_port_profile:
    scvmm_server: scvmm01.example.com
    name: Corp-Uplink
    state: absent
"""

RETURN = r"""
uplink_port_profile:
  description: Uplink port profile details.
  returned: when state is present
  type: dict
  sample:
    name: Corp-Uplink
    load_balancing_algorithm: Dynamic
"""
