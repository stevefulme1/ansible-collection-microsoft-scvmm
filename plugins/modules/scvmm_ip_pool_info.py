#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_ip_pool_info
short_description: Gather information about SCVMM static IP address pools
description:
  - Retrieve details of static IP address pools in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific IP pool. Omit to list all.
    type: str
  logical_network_definition:
    description:
      - Name of the logical network definition to filter pools by. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all IP pools
  microsoft.scvmm.scvmm_ip_pool_info:
    scvmm_server: scvmm01.example.com
  register: pools

- name: Get IP pools for a specific network definition
  microsoft.scvmm.scvmm_ip_pool_info:
    scvmm_server: scvmm01.example.com
    logical_network_definition: Corp-Site-A
  register: site_pools
"""

RETURN = r"""
pools:
  description: List of static IP address pool dictionaries.
  returned: always
  type: list
  elements: dict
"""
