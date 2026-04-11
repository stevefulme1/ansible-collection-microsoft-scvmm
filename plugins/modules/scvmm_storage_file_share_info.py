#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_file_share_info
short_description: Gather information about SCVMM storage file shares
description:
  - Retrieve details of storage file shares managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific file share. Omit to list all.
    type: str
  storage_provider:
    description:
      - Filter file shares by storage provider name.
    type: str
"""

EXAMPLES = r"""
- name: List all storage file shares
  microsoft.scvmm.scvmm_storage_file_share_info:
    scvmm_server: scvmm01.example.com
  register: file_shares

- name: Get file shares from a specific provider
  microsoft.scvmm.scvmm_storage_file_share_info:
    scvmm_server: scvmm01.example.com
    storage_provider: NetApp-SMIS
  register: provider_shares

- name: Get a specific file share
  microsoft.scvmm.scvmm_storage_file_share_info:
    scvmm_server: scvmm01.example.com
    name: Share-01
  register: share
"""

RETURN = r"""
file_shares:
  description: List of file share dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Share-01
      path: "\\\\storage01.example.com\\Share-01"
      capacity_gb: 1000
      free_space_gb: 750
"""
