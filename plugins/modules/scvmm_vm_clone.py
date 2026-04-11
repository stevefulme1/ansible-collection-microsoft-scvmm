#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_clone
short_description: Clone an existing SCVMM virtual machine
description:
  - Create a new virtual machine by cloning an existing VM in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  source_vm:
    description:
      - Name of the source virtual machine to clone.
    type: str
    required: true
  name:
    description:
      - Name for the new cloned virtual machine.
    type: str
    required: true
  cloud:
    description:
      - Name of the SCVMM cloud to place the cloned VM in.
    type: str
  host_group:
    description:
      - Host group where the cloned VM should be placed.
    type: str
  vm_host:
    description:
      - Specific Hyper-V host for the cloned VM.
    type: str
  description:
    description:
      - Description for the cloned virtual machine.
    type: str
"""

EXAMPLES = r"""
- name: Clone a VM to a specific host
  microsoft.scvmm.scvmm_vm_clone:
    scvmm_server: scvmm01.example.com
    source_vm: template-web-01
    name: web-server-02
    vm_host: hyperv01.example.com
    description: Cloned web server for staging

- name: Clone a VM into a cloud
  microsoft.scvmm.scvmm_vm_clone:
    scvmm_server: scvmm01.example.com
    source_vm: base-linux-vm
    name: linux-dev-01
    cloud: Development Cloud
"""

RETURN = r"""
vm:
  description: Details of the cloned virtual machine.
  returned: success
  type: dict
  sample:
    name: web-server-02
    source_vm: template-web-01
    vm_host: hyperv01.example.com
    status: Running
changed:
  description: Whether a new VM was created.
  returned: always
  type: bool
"""
