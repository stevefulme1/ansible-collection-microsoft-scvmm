#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_application_profile
short_description: Manage SCVMM application profiles
description:
  - Create, update, and remove application profiles in SCVMM.
  - Application profiles define application installation settings for VM service deployments.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the application profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the application profile.
    type: str
    choices: [present, absent]
    default: present
  compatibility_type:
    description:
      - Compatibility type for the application profile.
      - C(General) is used for standard applications.
      - C(SQLProfile) is used for SQL Server data-tier applications.
    type: str
    choices: [General, SQLProfile]
    default: General
  description:
    description:
      - Description of the application profile.
    type: str
"""

EXAMPLES = r"""
- name: Create a general application profile
  microsoft.scvmm.scvmm_application_profile:
    scvmm_server: scvmm01.example.com
    name: WebApp-Profile
    compatibility_type: General
    description: Profile for deploying web application components

- name: Create a SQL application profile
  microsoft.scvmm.scvmm_application_profile:
    scvmm_server: scvmm01.example.com
    name: SQL-DAC-Profile
    compatibility_type: SQLProfile
    description: SQL Server data-tier application profile

- name: Remove an application profile
  microsoft.scvmm.scvmm_application_profile:
    scvmm_server: scvmm01.example.com
    name: WebApp-Profile
    state: absent
"""

RETURN = r"""
profile:
  description: Details of the application profile.
  returned: when state is present
  type: dict
  sample:
    name: WebApp-Profile
    compatibility_type: General
    description: Profile for deploying web application components
changed:
  description: Whether the application profile was created, updated, or removed.
  returned: always
  type: bool
"""
