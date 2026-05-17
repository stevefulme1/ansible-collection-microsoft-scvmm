#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_pxe_server
short_description: Manage PXE servers in SCVMM
description:
  - Register or remove PXE servers used for bare metal provisioning in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - FQDN of the PXE server.
    type: str
    required: true
  state:
    description:
      - Desired state of the PXE server registration.
    type: str
    choices: [present, absent]
    default: present
  credential:
    description:
      - Credential name or run-as account used to connect to the PXE server.
    type: str
"""

EXAMPLES = r"""
- name: Register a PXE server
  microsoft.scvmm.scvmm_pxe_server:
    scvmm_server: scvmm01.example.com
    name: pxe01.example.com
    credential: pxe-runas

- name: Remove a PXE server
  microsoft.scvmm.scvmm_pxe_server:
    scvmm_server: scvmm01.example.com
    name: pxe01.example.com
    state: absent
"""

RETURN = r"""
pxe_server:
  description: PXE server details.
  returned: when state is present
  type: dict
"""
