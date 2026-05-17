#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_subnet_info
short_description: Gather information about SCVMM VM subnets
description:
  - Retrieve details of VM subnets in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_network:
    description:
      - Name of the VM network to filter subnets by. Omit to list all.
    type: str
  name:
    description:
      - Name of a specific VM subnet. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all VM subnets
  microsoft.scvmm.scvmm_vm_subnet_info:
    scvmm_server: scvmm01.example.com
  register: subnets

- name: Get subnets for a specific VM network
  microsoft.scvmm.scvmm_vm_subnet_info:
    scvmm_server: scvmm01.example.com
    vm_network: App-Network
  register: app_subnets
"""

RETURN = r"""
subnets:
  description: List of VM subnet dictionaries.
  returned: always
  type: list
  elements: dict
"""
