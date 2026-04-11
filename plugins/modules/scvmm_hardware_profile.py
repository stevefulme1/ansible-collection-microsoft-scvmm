#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_hardware_profile
short_description: Manage SCVMM hardware profiles
description:
  - Create, update, and remove hardware profiles in SCVMM.
  - Hardware profiles define CPU, memory, and other hardware settings for VM provisioning.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the hardware profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the hardware profile.
    type: str
    choices: [present, absent]
    default: present
  cpu_count:
    description:
      - Number of virtual CPUs to assign.
    type: int
  memory_mb:
    description:
      - Amount of static memory in megabytes.
    type: int
  dynamic_memory_enabled:
    description:
      - Whether to enable dynamic memory for the profile.
    type: bool
  description:
    description:
      - Description of the hardware profile.
    type: str
"""

EXAMPLES = r"""
- name: Create a hardware profile with 4 CPUs and 8 GB RAM
  microsoft.scvmm.scvmm_hardware_profile:
    scvmm_server: scvmm01.example.com
    name: Standard-4CPU-8GB
    cpu_count: 4
    memory_mb: 8192
    description: Standard profile for web servers

- name: Create a hardware profile with dynamic memory
  microsoft.scvmm.scvmm_hardware_profile:
    scvmm_server: scvmm01.example.com
    name: Dynamic-2CPU-4GB
    cpu_count: 2
    memory_mb: 4096
    dynamic_memory_enabled: true

- name: Remove a hardware profile
  microsoft.scvmm.scvmm_hardware_profile:
    scvmm_server: scvmm01.example.com
    name: Standard-4CPU-8GB
    state: absent
"""

RETURN = r"""
profile:
  description: Details of the hardware profile.
  returned: when state is present
  type: dict
  sample:
    name: Standard-4CPU-8GB
    cpu_count: 4
    memory_mb: 8192
    dynamic_memory_enabled: false
    description: Standard profile for web servers
changed:
  description: Whether the hardware profile was created, updated, or removed.
  returned: always
  type: bool
"""
