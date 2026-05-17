#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_sql_profile_info
short_description: Gather information about SCVMM SQL Server profiles
description:
  - Retrieve details of SQL Server profiles in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific SQL Server profile. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all SQL Server profiles
  microsoft.scvmm.scvmm_sql_profile_info:
    scvmm_server: scvmm01.example.com
  register: sql_profiles

- name: Get a specific SQL Server profile
  microsoft.scvmm.scvmm_sql_profile_info:
    scvmm_server: scvmm01.example.com
    name: AppDB-Profile
  register: profile
"""

RETURN = r"""
profiles:
  description: List of SQL Server profile dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: AppDB-Profile
      description: SQL profile for application database tier
      sql_instance_name: MSSQLSERVER
      deployment_order: 1
"""
