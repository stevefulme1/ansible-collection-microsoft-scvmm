#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_cloud_capacity
short_description: Set cloud capacity limits in SCVMM
description:
  - Configure capacity limits for a private cloud in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  cloud:
    description:
      - Name of the cloud to set capacity limits on.
    type: str
    required: true
  cpu_count:
    description:
      - Maximum number of virtual CPUs allowed in the cloud.
    type: int
  memory_mb:
    description:
      - Maximum amount of memory in megabytes allowed in the cloud.
    type: int
  storage_gb:
    description:
      - Maximum amount of storage in gigabytes allowed in the cloud.
    type: int
  vm_count:
    description:
      - Maximum number of virtual machines allowed in the cloud.
    type: int
  custom_quota_count:
    description:
      - Maximum custom quota points allowed in the cloud.
    type: int
"""

EXAMPLES = r"""
- name: Set capacity limits on a cloud
  microsoft.scvmm.scvmm_cloud_capacity:
    scvmm_server: scvmm01.example.com
    cloud: Production
    cpu_count: 200
    memory_mb: 524288
    storage_gb: 10240
    vm_count: 100

- name: Update only VM count limit
  microsoft.scvmm.scvmm_cloud_capacity:
    scvmm_server: scvmm01.example.com
    cloud: Development
    vm_count: 50
    custom_quota_count: 500
"""

RETURN = r"""
capacity:
  description: Cloud capacity settings after the operation.
  returned: always
  type: dict
"""
