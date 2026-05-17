#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_uplink_port_profile_info
short_description: Gather information about SCVMM native uplink port profiles
description:
  - Retrieve details of native uplink port profiles in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific uplink port profile. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all uplink port profiles
  microsoft.scvmm.scvmm_uplink_port_profile_info:
    scvmm_server: scvmm01.example.com
  register: profiles

- name: Get a specific uplink port profile
  microsoft.scvmm.scvmm_uplink_port_profile_info:
    scvmm_server: scvmm01.example.com
    name: Corp-Uplink
  register: corp_uplink
"""

RETURN = r"""
profiles:
  description: List of uplink port profile dictionaries.
  returned: always
  type: list
  elements: dict
"""
