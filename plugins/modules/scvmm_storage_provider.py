#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_provider
short_description: Register and manage SCVMM storage providers
description:
  - Add, update, or remove storage providers (SMI-S or SMP) in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the storage provider.
    type: str
    required: true
  state:
    description:
      - Desired state of the storage provider.
    type: str
    choices: [present, absent]
    default: present
  computer_name:
    description:
      - FQDN or IP address of the storage provider host.
      - Required when I(state=present).
    type: str
  credential:
    description:
      - Name of the Run As account to use when connecting to the provider.
    type: str
  provider_type:
    description:
      - Type of storage provider to register.
    type: str
    choices: [SMIS, SMP]
"""

EXAMPLES = r"""
- name: Register an SMI-S storage provider
  microsoft.scvmm.scvmm_storage_provider:
    scvmm_server: scvmm01.example.com
    name: NetApp-SMIS
    computer_name: storage01.example.com
    provider_type: SMIS
    credential: StorageRunAs

- name: Remove a storage provider
  microsoft.scvmm.scvmm_storage_provider:
    scvmm_server: scvmm01.example.com
    name: NetApp-SMIS
    state: absent
"""

RETURN = r"""
storage_provider:
  description: Storage provider details.
  returned: when state is present
  type: dict
  sample:
    name: NetApp-SMIS
    computer_name: storage01.example.com
    provider_type: SMIS
    status: Responding
"""
