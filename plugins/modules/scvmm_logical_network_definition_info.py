#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_network_definition_info
short_description: Gather information about SCVMM logical network definitions
description:
  - Retrieve details of logical network definitions (network sites) in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  logical_network:
    description:
      - Name of the logical network to filter definitions by. Omit to list all.
    type: str
  name:
    description:
      - Name of a specific logical network definition. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all logical network definitions
  microsoft.scvmm.scvmm_logical_network_definition_info:
    scvmm_server: scvmm01.example.com
  register: net_defs

- name: Get definitions for a specific logical network
  microsoft.scvmm.scvmm_logical_network_definition_info:
    scvmm_server: scvmm01.example.com
    logical_network: Corp-Network
  register: corp_defs
"""

RETURN = r"""
definitions:
  description: List of logical network definition dictionaries.
  returned: always
  type: list
  elements: dict
"""
