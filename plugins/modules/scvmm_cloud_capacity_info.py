#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_cloud_capacity_info
short_description: Gather cloud capacity and usage information from SCVMM
description:
  - Retrieve capacity limits and current usage for a private cloud in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  cloud:
    description:
      - Name of the cloud to retrieve capacity information for.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Get capacity and usage for a cloud
  microsoft.scvmm.scvmm_cloud_capacity_info:
    scvmm_server: scvmm01.example.com
    cloud: Production
  register: capacity
"""

RETURN = r"""
capacity:
  description: Cloud capacity dictionary with limits and current usage.
  returned: always
  type: dict
  sample:
    cpu_count: 200
    cpu_used: 84
    memory_mb: 524288
    memory_used_mb: 212992
    storage_gb: 10240
    storage_used_gb: 4096
    vm_count: 100
    vm_used: 42
"""
