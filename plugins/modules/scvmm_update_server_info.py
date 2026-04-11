#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_update_server_info
short_description: Gather information about SCVMM update servers
description:
  - Retrieve details of registered WSUS update servers in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - FQDN of a specific update server. Omit to list all update servers.
    type: str
"""

EXAMPLES = r"""
- name: List all update servers
  microsoft.scvmm.scvmm_update_server_info:
    scvmm_server: scvmm01.example.com
  register: update_servers

- name: Get a specific update server
  microsoft.scvmm.scvmm_update_server_info:
    scvmm_server: scvmm01.example.com
    name: wsus01.example.com
  register: update_server
"""

RETURN = r"""
servers:
  description: List of update server dictionaries.
  returned: always
  type: list
  elements: dict
"""
