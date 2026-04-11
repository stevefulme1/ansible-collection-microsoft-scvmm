#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_pool
short_description: Manage SCVMM storage pools
description:
  - Configure storage pools on managed hosts in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the storage pool.
    type: str
    required: true
  storage_classification:
    description:
      - Storage classification to assign to the pool.
    type: str
  host:
    description:
      - Name of the host that owns the storage pool.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Configure a storage pool
  microsoft.scvmm.scvmm_storage_pool:
    scvmm_server: scvmm01.example.com
    name: Pool-01
    host: hyperv01.example.com
    storage_classification: Gold-Storage

- name: Update storage pool classification
  microsoft.scvmm.scvmm_storage_pool:
    scvmm_server: scvmm01.example.com
    name: Pool-01
    host: hyperv01.example.com
    storage_classification: Silver-Storage
"""

RETURN = r"""
storage_pool:
  description: Storage pool details.
  returned: always
  type: dict
  sample:
    name: Pool-01
    host: hyperv01.example.com
    storage_classification: Gold-Storage
    capacity_gb: 500
"""
