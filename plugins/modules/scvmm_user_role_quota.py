#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_user_role_quota
short_description: Set user role quotas per cloud in SCVMM
description:
  - Configure resource quotas for a user role within a specific cloud.
  - Quotas limit the amount of CPU, memory, storage, and VMs a role can consume.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  user_role:
    description:
      - Name of the user role to set quotas for.
    type: str
    required: true
  cloud:
    description:
      - Name of the cloud where the quota applies.
    type: str
    required: true
  cpu_count:
    description:
      - Maximum number of virtual CPUs allowed.
    type: int
  memory_mb:
    description:
      - Maximum memory in megabytes allowed.
    type: int
  storage_gb:
    description:
      - Maximum storage in gigabytes allowed.
    type: int
  vm_count:
    description:
      - Maximum number of virtual machines allowed.
    type: int
  custom_quota_count:
    description:
      - Maximum count for custom quota points.
    type: int
"""

EXAMPLES = r"""
- name: Set quotas for a self-service role in a cloud
  microsoft.scvmm.scvmm_user_role_quota:
    scvmm_server: scvmm01.example.com
    user_role: Dev-Team-Role
    cloud: Development-Cloud
    cpu_count: 64
    memory_mb: 131072
    storage_gb: 2048
    vm_count: 20

- name: Set only VM count quota
  microsoft.scvmm.scvmm_user_role_quota:
    scvmm_server: scvmm01.example.com
    user_role: QA-Role
    cloud: QA-Cloud
    vm_count: 10
"""

RETURN = r"""
quota:
  description: Quota details after update.
  returned: always
  type: dict
  sample:
    user_role: Dev-Team-Role
    cloud: Development-Cloud
    cpu_count: 64
    memory_mb: 131072
    storage_gb: 2048
    vm_count: 20
"""
