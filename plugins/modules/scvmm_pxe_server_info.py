#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_pxe_server_info
short_description: Gather information about SCVMM PXE servers
description:
  - Retrieve details of registered PXE servers in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - FQDN of a specific PXE server. Omit to list all PXE servers.
    type: str
"""

EXAMPLES = r"""
- name: List all PXE servers
  microsoft.scvmm.scvmm_pxe_server_info:
    scvmm_server: scvmm01.example.com
  register: pxe_servers

- name: Get a specific PXE server
  microsoft.scvmm.scvmm_pxe_server_info:
    scvmm_server: scvmm01.example.com
    name: pxe01.example.com
  register: pxe_server
"""

RETURN = r"""
servers:
  description: List of PXE server dictionaries.
  returned: always
  type: list
  elements: dict
"""
