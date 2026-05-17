#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm
short_description: Manage virtual machines in Microsoft SCVMM
description:
  - Create, modify, and remove virtual machines managed by
    Microsoft System Center Virtual Machine Manager (SCVMM).
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  state:
    description:
      - Desired state of the virtual machine.
    type: str
    choices: [present, absent]
    default: present
  template:
    description:
      - Name of the VM template to use when creating a new VM.
      - Required when I(state=present) and the VM does not exist.
    type: str
  cloud:
    description:
      - Name of the SCVMM cloud to deploy the VM into.
    type: str
  host_group:
    description:
      - Host group path for VM placement.
    type: str
  vm_host:
    description:
      - Specific Hyper-V host to place the VM on.
      - Mutually exclusive with I(cloud).
    type: str
  cpu_count:
    description:
      - Number of virtual CPUs.
    type: int
  memory_mb:
    description:
      - Amount of memory in megabytes.
    type: int
  description:
    description:
      - Description of the virtual machine.
    type: str
  start_action:
    description:
      - Action to take when the Hyper-V host starts.
    type: str
    choices: [NeverAutoTurnOnVM, AlwaysAutoTurnOnVM, TurnOnVMIfRunningWhenVSStopped]
  stop_action:
    description:
      - Action to take when the Hyper-V host stops.
    type: str
    choices: [SaveVM, TurnOffVM, ShutdownGuestOS]
"""

EXAMPLES = r"""
- name: Create a VM from template
  microsoft.scvmm.scvmm_vm:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    state: present
    template: Windows2022-Standard
    cloud: Production
    cpu_count: 4
    memory_mb: 8192
    description: Production web server

- name: Remove a VM
  microsoft.scvmm.scvmm_vm:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    state: absent
"""

RETURN = r"""
vm:
  description: Dictionary of VM properties.
  returned: when state is present
  type: dict
  sample:
    name: web-server-01
    status: Running
    cpu_count: 4
    memory_mb: 8192
    cloud: Production
"""
