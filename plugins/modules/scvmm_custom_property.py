#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_custom_property
short_description: Manage custom property definitions in SCVMM
description:
  - Create, modify, and remove custom property definitions used to tag SCVMM objects.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the custom property.
    type: str
    required: true
  state:
    description:
      - Desired state of the custom property.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the custom property.
    type: str
  member_type:
    description:
      - Object type the custom property applies to.
    type: str
    choices: [VM, VMHost, Cloud, VMTemplate, ServiceTemplate, ServiceInstance]
"""

EXAMPLES = r"""
- name: Create a custom property for VMs
  microsoft.scvmm.scvmm_custom_property:
    scvmm_server: scvmm01.example.com
    name: CostCenter
    description: Cost center code for chargeback
    member_type: VM

- name: Create a custom property for hosts
  microsoft.scvmm.scvmm_custom_property:
    scvmm_server: scvmm01.example.com
    name: RackLocation
    description: Physical rack location
    member_type: VMHost

- name: Remove a custom property
  microsoft.scvmm.scvmm_custom_property:
    scvmm_server: scvmm01.example.com
    name: CostCenter
    state: absent
"""

RETURN = r"""
custom_property:
  description: Custom property details.
  returned: when state is present
  type: dict
"""
