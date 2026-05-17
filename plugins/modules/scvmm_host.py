#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host
short_description: Manage Hyper-V hosts in SCVMM
description:
  - Add, configure, and remove Hyper-V hosts managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Fully qualified domain name of the Hyper-V host.
    type: str
    required: true
  state:
    description:
      - Desired state of the host in SCVMM.
    type: str
    choices: [present, absent]
    default: present
  credential:
    description:
      - Name of the RunAs account used to manage the host.
    type: str
  host_group:
    description:
      - Host group path where the host should be placed.
      - Required when I(state=present).
    type: str
  reassociate:
    description:
      - Whether to reassociate the host if it already exists in a different state.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Add a Hyper-V host to SCVMM
  microsoft.scvmm.scvmm_host:
    scvmm_server: scvmm01.example.com
    name: hyperv01.example.com
    host_group: All Hosts\\Production
    credential: HostRunAs

- name: Reassociate an existing host
  microsoft.scvmm.scvmm_host:
    scvmm_server: scvmm01.example.com
    name: hyperv01.example.com
    host_group: All Hosts\\Production
    credential: HostRunAs
    reassociate: true

- name: Remove a Hyper-V host from SCVMM
  microsoft.scvmm.scvmm_host:
    scvmm_server: scvmm01.example.com
    name: hyperv01.example.com
    state: absent
"""

RETURN = r"""
host:
  description: Host details after the operation.
  returned: when state is present
  type: dict
"""
