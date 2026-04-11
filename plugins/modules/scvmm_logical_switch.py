#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_switch
short_description: Manage SCVMM logical switches
description:
  - Create, modify, and remove logical switches in SCVMM.
  - Logical switches aggregate port profiles and network policies for Hyper-V hosts.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the logical switch.
    type: str
    required: true
  state:
    description:
      - Desired state of the logical switch.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the logical switch.
    type: str
  uplink_port_profile:
    description:
      - Name of the uplink port profile to associate with the logical switch.
    type: str
  enable_sr_iov:
    description:
      - Enable Single-Root I/O Virtualization (SR-IOV) on the logical switch.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Create a logical switch
  microsoft.scvmm.scvmm_logical_switch:
    scvmm_server: scvmm01.example.com
    name: Prod-Switch
    description: Production logical switch
    uplink_port_profile: Corp-Uplink
    enable_sr_iov: true

- name: Remove a logical switch
  microsoft.scvmm.scvmm_logical_switch:
    scvmm_server: scvmm01.example.com
    name: Prod-Switch
    state: absent
"""

RETURN = r"""
logical_switch:
  description: Logical switch details.
  returned: when state is present
  type: dict
  sample:
    name: Prod-Switch
    description: Production logical switch
"""
