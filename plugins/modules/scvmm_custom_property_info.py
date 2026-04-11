#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_custom_property_info
short_description: Gather information about SCVMM custom property definitions
description:
  - Retrieve details of custom property definitions configured in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific custom property. Omit to list all custom properties.
    type: str
  member_type:
    description:
      - Filter custom properties by member type.
    type: str
    choices: [VM, VMHost, Cloud, VMTemplate, ServiceTemplate, ServiceInstance]
"""

EXAMPLES = r"""
- name: List all custom properties
  microsoft.scvmm.scvmm_custom_property_info:
    scvmm_server: scvmm01.example.com
  register: properties

- name: Get custom properties for VMs only
  microsoft.scvmm.scvmm_custom_property_info:
    scvmm_server: scvmm01.example.com
    member_type: VM
  register: vm_properties
"""

RETURN = r"""
properties:
  description: List of custom property dictionaries.
  returned: always
  type: list
  elements: dict
"""
