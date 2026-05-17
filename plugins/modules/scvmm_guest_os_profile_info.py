#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_guest_os_profile_info
short_description: Gather information about SCVMM guest OS profiles
description:
  - Retrieve details of guest OS profiles from SCVMM.
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
      - Name of a specific guest OS profile to retrieve.
      - If omitted, all guest OS profiles are returned.
    type: str
"""

EXAMPLES = r"""
- name: Get all guest OS profiles
  microsoft.scvmm.scvmm_guest_os_profile_info:
    scvmm_server: scvmm01.example.com
  register: os_profiles

- name: Get a specific guest OS profile
  microsoft.scvmm.scvmm_guest_os_profile_info:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Standard
  register: os_profile
"""

RETURN = r"""
profiles:
  description: List of guest OS profiles.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Windows2022-Standard
      operating_system: Windows Server 2022 Datacenter
      computer_name_pattern: "WEB-###"
      domain: example.com
      description: Standard Windows Server 2022 guest profile
    - name: RHEL9-Standard
      operating_system: "Red Hat Enterprise Linux 9 (64 bit)"
      computer_name_pattern: "LNX-###"
      domain: ""
      description: Standard RHEL 9 guest profile
"""
