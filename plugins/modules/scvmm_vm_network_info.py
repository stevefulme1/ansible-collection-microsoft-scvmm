#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_network_info
short_description: Gather information about SCVMM VM networks
description:
  - Retrieve details of VM networks in SCVMM.
  - Can filter by name or logical network.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific VM network. Omit to list all.
    type: str
  logical_network:
    description:
      - Filter VM networks by logical network name.
    type: str
"""

EXAMPLES = r"""
- name: List all VM networks
  microsoft.scvmm.scvmm_vm_network_info:
    scvmm_server: scvmm01.example.com
  register: vm_networks

- name: Get a specific VM network
  microsoft.scvmm.scvmm_vm_network_info:
    scvmm_server: scvmm01.example.com
    name: App-Network
  register: vm_network
"""

RETURN = r"""
vm_networks:
  description: List of VM network dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: App-Network
      logical_network: Corp-Network
      isolation_type: NoIsolation
"""
