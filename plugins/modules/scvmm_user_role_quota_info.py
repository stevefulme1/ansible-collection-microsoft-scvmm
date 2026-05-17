#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_user_role_quota_info
short_description: Gather information about SCVMM user role quotas
description:
  - Retrieve quota details for user roles in SCVMM clouds.
  - Can filter by user role, cloud, or both.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  user_role:
    description:
      - Name of a specific user role to filter quotas. Omit to list all.
    type: str
  cloud:
    description:
      - Name of a specific cloud to filter quotas. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all user role quotas
  microsoft.scvmm.scvmm_user_role_quota_info:
    scvmm_server: scvmm01.example.com
  register: all_quotas

- name: Get quotas for a specific role and cloud
  microsoft.scvmm.scvmm_user_role_quota_info:
    scvmm_server: scvmm01.example.com
    user_role: Dev-Team-Role
    cloud: Development-Cloud
  register: quota
"""

RETURN = r"""
quotas:
  description: List of user role quota dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - user_role: Dev-Team-Role
      cloud: Development-Cloud
      cpu_count: 64
      memory_mb: 131072
      storage_gb: 2048
      vm_count: 20
"""
