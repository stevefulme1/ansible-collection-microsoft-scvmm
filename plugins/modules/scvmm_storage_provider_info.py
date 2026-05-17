#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_provider_info
short_description: Gather information about SCVMM storage providers
description:
  - Retrieve details of storage providers registered in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific storage provider. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all storage providers
  microsoft.scvmm.scvmm_storage_provider_info:
    scvmm_server: scvmm01.example.com
  register: providers

- name: Get a specific storage provider
  microsoft.scvmm.scvmm_storage_provider_info:
    scvmm_server: scvmm01.example.com
    name: NetApp-SMIS
  register: provider
"""

RETURN = r"""
providers:
  description: List of storage provider dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: NetApp-SMIS
      computer_name: storage01.example.com
      provider_type: SMIS
      status: Responding
"""
