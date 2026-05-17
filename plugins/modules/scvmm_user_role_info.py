#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_user_role_info
short_description: Gather information about SCVMM user roles
description:
  - Retrieve details of user roles in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific user role. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all user roles
  microsoft.scvmm.scvmm_user_role_info:
    scvmm_server: scvmm01.example.com
  register: user_roles

- name: Get a specific user role
  microsoft.scvmm.scvmm_user_role_info:
    scvmm_server: scvmm01.example.com
    name: Dev-Team-Role
  register: role
"""

RETURN = r"""
user_roles:
  description: List of user role dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Dev-Team-Role
      profile: SelfServiceUser
      description: Role for development team
      members:
        - DOMAIN\\dev-team
"""
