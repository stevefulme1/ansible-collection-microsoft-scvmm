#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_mac_address_pool
short_description: Manage SCVMM MAC address pools
description:
  - Create, modify, and remove MAC address pools in SCVMM.
  - MAC address pools provide automatic MAC address assignment for virtual network adapters.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the MAC address pool.
    type: str
    required: true
  state:
    description:
      - Desired state of the MAC address pool.
    type: str
    choices: [present, absent]
    default: present
  mac_address_range_start:
    description:
      - Starting MAC address of the pool range (e.g. C(00:1D:D8:B7:1C:00)).
      - Required when I(state=present).
    type: str
  mac_address_range_end:
    description:
      - Ending MAC address of the pool range (e.g. C(00:1D:D8:F4:1F:FF)).
      - Required when I(state=present).
    type: str
  description:
    description:
      - Description of the MAC address pool.
    type: str
"""

EXAMPLES = r"""
- name: Create a MAC address pool
  microsoft.scvmm.scvmm_mac_address_pool:
    scvmm_server: scvmm01.example.com
    name: Prod-MAC-Pool
    mac_address_range_start: "00:1D:D8:B7:1C:00"
    mac_address_range_end: "00:1D:D8:F4:1F:FF"
    description: Production MAC pool

- name: Remove a MAC address pool
  microsoft.scvmm.scvmm_mac_address_pool:
    scvmm_server: scvmm01.example.com
    name: Prod-MAC-Pool
    state: absent
"""

RETURN = r"""
mac_address_pool:
  description: MAC address pool details.
  returned: when state is present
  type: dict
  sample:
    name: Prod-MAC-Pool
    mac_address_range_start: "00:1D:D8:B7:1C:00"
    mac_address_range_end: "00:1D:D8:F4:1F:FF"
"""
