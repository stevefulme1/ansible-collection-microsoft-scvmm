#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_user_role
short_description: Manage SCVMM user roles
description:
  - Create, modify, and remove user roles in SCVMM.
  - User roles control RBAC permissions for SCVMM operations.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the user role.
    type: str
    required: true
  state:
    description:
      - Desired state of the user role.
    type: str
    choices: [present, absent]
    default: present
  profile:
    description:
      - User role profile type.
    type: str
    choices: [Administrator, DelegatedAdmin, ReadOnlyAdmin, SelfServiceUser, TenantAdmin]
  description:
    description:
      - Description of the user role.
    type: str
  members:
    description:
      - List of Active Directory accounts to add to the role.
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: Create a self-service user role
  microsoft.scvmm.scvmm_user_role:
    scvmm_server: scvmm01.example.com
    name: Dev-Team-Role
    profile: SelfServiceUser
    description: Role for development team
    members:
      - DOMAIN\\dev-team

- name: Remove a user role
  microsoft.scvmm.scvmm_user_role:
    scvmm_server: scvmm01.example.com
    name: Dev-Team-Role
    state: absent
"""

RETURN = r"""
user_role:
  description: User role details.
  returned: when state is present
  type: dict
  sample:
    name: Dev-Team-Role
    profile: SelfServiceUser
    description: Role for development team
"""
