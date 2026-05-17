#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_run_as_account_info
short_description: Gather information about SCVMM RunAs accounts
description:
  - Retrieve details of RunAs accounts in SCVMM.
  - Passwords are never returned in the output.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific RunAs account. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all RunAs accounts
  microsoft.scvmm.scvmm_run_as_account_info:
    scvmm_server: scvmm01.example.com
  register: run_as_accounts

- name: Get a specific RunAs account
  microsoft.scvmm.scvmm_run_as_account_info:
    scvmm_server: scvmm01.example.com
    name: fabric-admin
  register: account
"""

RETURN = r"""
accounts:
  description: List of RunAs account dictionaries (passwords are excluded).
  returned: always
  type: list
  elements: dict
  sample:
    - name: fabric-admin
      credential_type: WindowsCredential
      username: DOMAIN\\svc-fabric
      description: Fabric administration credentials
"""
