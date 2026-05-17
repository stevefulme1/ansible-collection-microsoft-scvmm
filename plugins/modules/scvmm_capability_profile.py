#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_capability_profile
short_description: Manage SCVMM capability profiles
description:
  - Create, update, and remove capability profiles in SCVMM.
  - Capability profiles define the capabilities and constraints available to VMs deployed in a cloud.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the capability profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the capability profile.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the capability profile.
    type: str
  fabric_capability:
    description:
      - Fabric capability type for the profile, such as C(HyperV) or C(ESX).
    type: str
"""

EXAMPLES = r"""
- name: Create a Hyper-V capability profile
  microsoft.scvmm.scvmm_capability_profile:
    scvmm_server: scvmm01.example.com
    name: HyperV-Gen2
    fabric_capability: HyperV
    description: Capability profile for Generation 2 Hyper-V VMs

- name: Remove a capability profile
  microsoft.scvmm.scvmm_capability_profile:
    scvmm_server: scvmm01.example.com
    name: HyperV-Gen2
    state: absent
"""

RETURN = r"""
profile:
  description: Details of the capability profile.
  returned: when state is present
  type: dict
  sample:
    name: HyperV-Gen2
    fabric_capability: HyperV
    description: Capability profile for Generation 2 Hyper-V VMs
changed:
  description: Whether the capability profile was created, updated, or removed.
  returned: always
  type: bool
"""
