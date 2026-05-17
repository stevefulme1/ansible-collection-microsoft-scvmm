#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_hardware_profile_info
short_description: Gather information about SCVMM hardware profiles
description:
  - Retrieve details of hardware profiles from SCVMM.
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
      - Name of a specific hardware profile to retrieve.
      - If omitted, all hardware profiles are returned.
    type: str
"""

EXAMPLES = r"""
- name: Get all hardware profiles
  microsoft.scvmm.scvmm_hardware_profile_info:
    scvmm_server: scvmm01.example.com
  register: hw_profiles

- name: Get a specific hardware profile
  microsoft.scvmm.scvmm_hardware_profile_info:
    scvmm_server: scvmm01.example.com
    name: Standard-4CPU-8GB
  register: hw_profile
"""

RETURN = r"""
profiles:
  description: List of hardware profiles.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Standard-4CPU-8GB
      cpu_count: 4
      memory_mb: 8192
      dynamic_memory_enabled: false
      description: Standard profile for web servers
    - name: Dynamic-2CPU-4GB
      cpu_count: 2
      memory_mb: 4096
      dynamic_memory_enabled: true
      description: ""
"""
