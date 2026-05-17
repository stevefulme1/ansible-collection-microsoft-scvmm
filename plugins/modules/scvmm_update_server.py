#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_update_server
short_description: Manage WSUS update servers in SCVMM
description:
  - Register or remove WSUS update servers used for patch management in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - FQDN of the WSUS update server.
    type: str
    required: true
  state:
    description:
      - Desired state of the update server registration.
    type: str
    choices: [present, absent]
    default: present
  credential:
    description:
      - Credential name or run-as account used to connect to the WSUS server.
    type: str
  port:
    description:
      - Port number used to connect to the WSUS server.
    type: int
    default: 8530
  use_ssl:
    description:
      - Whether to use SSL when connecting to the WSUS server.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Register a WSUS update server
  microsoft.scvmm.scvmm_update_server:
    scvmm_server: scvmm01.example.com
    name: wsus01.example.com
    port: 8530
    use_ssl: false

- name: Register a WSUS server with SSL and credentials
  microsoft.scvmm.scvmm_update_server:
    scvmm_server: scvmm01.example.com
    name: wsus01.example.com
    credential: wsus-runas
    port: 8531
    use_ssl: true

- name: Remove a WSUS update server
  microsoft.scvmm.scvmm_update_server:
    scvmm_server: scvmm01.example.com
    name: wsus01.example.com
    state: absent
"""

RETURN = r"""
update_server:
  description: Update server details.
  returned: when state is present
  type: dict
"""
