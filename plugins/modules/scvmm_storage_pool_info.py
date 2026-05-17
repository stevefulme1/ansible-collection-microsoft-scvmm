#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_pool_info
short_description: Gather information about SCVMM storage pools
description:
  - Retrieve details of storage pools managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific storage pool. Omit to list all.
    type: str
  host:
    description:
      - Filter storage pools by host name.
    type: str
"""

EXAMPLES = r"""
- name: List all storage pools
  microsoft.scvmm.scvmm_storage_pool_info:
    scvmm_server: scvmm01.example.com
  register: pools

- name: Get storage pools on a specific host
  microsoft.scvmm.scvmm_storage_pool_info:
    scvmm_server: scvmm01.example.com
    host: hyperv01.example.com
  register: host_pools

- name: Get a specific storage pool
  microsoft.scvmm.scvmm_storage_pool_info:
    scvmm_server: scvmm01.example.com
    name: Pool-01
    host: hyperv01.example.com
  register: pool
"""

RETURN = r"""
pools:
  description: List of storage pool dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Pool-01
      host: hyperv01.example.com
      storage_classification: Gold-Storage
      capacity_gb: 500
      free_space_gb: 350
"""
