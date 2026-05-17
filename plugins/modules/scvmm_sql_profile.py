#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_sql_profile
short_description: Manage SCVMM SQL Server profiles
description:
  - Create, modify, and remove SQL Server profiles in SCVMM.
  - SQL profiles define SQL Server deployment configurations for service templates.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the SQL Server profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the SQL Server profile.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the SQL Server profile.
    type: str
  sql_instance_name:
    description:
      - Name of the SQL Server instance.
    type: str
  deployment_order:
    description:
      - Order in which the SQL profile is deployed within a service template.
    type: int
"""

EXAMPLES = r"""
- name: Create a SQL Server profile
  microsoft.scvmm.scvmm_sql_profile:
    scvmm_server: scvmm01.example.com
    name: AppDB-Profile
    description: SQL profile for application database tier
    sql_instance_name: MSSQLSERVER
    deployment_order: 1

- name: Update a SQL Server profile
  microsoft.scvmm.scvmm_sql_profile:
    scvmm_server: scvmm01.example.com
    name: AppDB-Profile
    deployment_order: 2

- name: Remove a SQL Server profile
  microsoft.scvmm.scvmm_sql_profile:
    scvmm_server: scvmm01.example.com
    name: AppDB-Profile
    state: absent
"""

RETURN = r"""
sql_profile:
  description: SQL Server profile details.
  returned: when state is present
  type: dict
  sample:
    name: AppDB-Profile
    description: SQL profile for application database tier
    sql_instance_name: MSSQLSERVER
    deployment_order: 1
"""
