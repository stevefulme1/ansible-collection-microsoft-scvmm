#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_switch_info
short_description: Gather information about SCVMM logical switches
description:
  - Retrieve details of logical switches in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific logical switch. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all logical switches
  microsoft.scvmm.scvmm_logical_switch_info:
    scvmm_server: scvmm01.example.com
  register: switches

- name: Get a specific logical switch
  microsoft.scvmm.scvmm_logical_switch_info:
    scvmm_server: scvmm01.example.com
    name: Prod-Switch
  register: prod_switch
"""

RETURN = r"""
switches:
  description: List of logical switch dictionaries.
  returned: always
  type: list
  elements: dict
"""
