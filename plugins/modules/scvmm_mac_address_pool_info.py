#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_mac_address_pool_info
short_description: Gather information about SCVMM MAC address pools
description:
  - Retrieve details of MAC address pools in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific MAC address pool. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all MAC address pools
  microsoft.scvmm.scvmm_mac_address_pool_info:
    scvmm_server: scvmm01.example.com
  register: pools

- name: Get a specific MAC address pool
  microsoft.scvmm.scvmm_mac_address_pool_info:
    scvmm_server: scvmm01.example.com
    name: Prod-MAC-Pool
  register: prod_pool
"""

RETURN = r"""
pools:
  description: List of MAC address pool dictionaries.
  returned: always
  type: list
  elements: dict
"""
