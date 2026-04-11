#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_physical_computer_profile_info
short_description: Gather information about SCVMM physical computer profiles
description:
  - Retrieve details of physical computer profiles used for bare metal provisioning.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific profile. Omit to list all profiles.
    type: str
"""

EXAMPLES = r"""
- name: List all physical computer profiles
  microsoft.scvmm.scvmm_physical_computer_profile_info:
    scvmm_server: scvmm01.example.com
  register: profiles

- name: Get a specific profile
  microsoft.scvmm.scvmm_physical_computer_profile_info:
    scvmm_server: scvmm01.example.com
    name: HyperV-Server-2025
  register: profile
"""

RETURN = r"""
profiles:
  description: List of physical computer profile dictionaries.
  returned: always
  type: list
  elements: dict
"""
