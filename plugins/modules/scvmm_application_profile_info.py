#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_application_profile_info
short_description: Gather information about SCVMM application profiles
description:
  - Retrieve details of application profiles from SCVMM.
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
      - Name of a specific application profile to retrieve.
      - If omitted, all application profiles are returned.
    type: str
"""

EXAMPLES = r"""
- name: Get all application profiles
  microsoft.scvmm.scvmm_application_profile_info:
    scvmm_server: scvmm01.example.com
  register: app_profiles

- name: Get a specific application profile
  microsoft.scvmm.scvmm_application_profile_info:
    scvmm_server: scvmm01.example.com
    name: WebApp-Profile
  register: app_profile
"""

RETURN = r"""
profiles:
  description: List of application profiles.
  returned: always
  type: list
  elements: dict
  sample:
    - name: WebApp-Profile
      compatibility_type: General
      description: Profile for deploying web application components
    - name: SQL-DAC-Profile
      compatibility_type: SQLProfile
      description: SQL Server data-tier application profile
"""
