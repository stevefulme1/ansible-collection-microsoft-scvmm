#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_capability_profile_info
short_description: Gather information about SCVMM capability profiles
description:
  - Retrieve details of capability profiles from SCVMM.
  - Can return all profiles or filter by name.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific capability profile to retrieve.
      - If omitted, all capability profiles are returned.
    type: str
"""

EXAMPLES = r"""
- name: Get all capability profiles
  microsoft.scvmm.scvmm_capability_profile_info:
    scvmm_server: scvmm01.example.com
  register: cap_profiles

- name: Get a specific capability profile
  microsoft.scvmm.scvmm_capability_profile_info:
    scvmm_server: scvmm01.example.com
    name: HyperV-Gen2
  register: cap_profile
"""

RETURN = r"""
profiles:
  description: List of capability profiles.
  returned: always
  type: list
  elements: dict
  sample:
    - name: HyperV-Gen2
      fabric_capability: HyperV
      description: Capability profile for Generation 2 Hyper-V VMs
    - name: HyperV-Gen1
      fabric_capability: HyperV
      description: Capability profile for Generation 1 Hyper-V VMs
"""
