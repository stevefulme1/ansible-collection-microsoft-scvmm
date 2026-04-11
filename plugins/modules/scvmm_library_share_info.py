#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_library_share_info
short_description: Gather information about SCVMM library shares
description:
  - Retrieve details of library shares configured in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  library_server:
    description:
      - Filter library shares by library server FQDN.
    type: str
  name:
    description:
      - Name of a specific library share. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all library shares
  microsoft.scvmm.scvmm_library_share_info:
    scvmm_server: scvmm01.example.com
  register: shares

- name: Get library shares on a specific server
  microsoft.scvmm.scvmm_library_share_info:
    scvmm_server: scvmm01.example.com
    library_server: lib01.example.com
  register: server_shares

- name: Get a specific library share
  microsoft.scvmm.scvmm_library_share_info:
    scvmm_server: scvmm01.example.com
    name: MSSCVMMLibrary
  register: share
"""

RETURN = r"""
shares:
  description: List of library share dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: MSSCVMMLibrary
      path: "\\\\lib01.example.com\\MSSCVMMLibrary"
      library_server: lib01.example.com
      description: Default VMM library share
"""
